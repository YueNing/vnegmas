import itertools
# from negmas.helpers import ConfigReader, LoggerMixin
import logging
from abc import ABC, abstractmethod
from collections import defaultdict

from negmas import (AgentMechanismInterface, Breach, Contract, MechanismState,
                    Negotiator, RenegotiationRequest, UtilityFunction)
from negmas.apps.scml import DoNothingFactoryManager, FactoryManager
from negmas.apps.scml.awi import SCMLAWI, _ShadowSCMLAWI
from negmas.apps.scml.common import (CFP, INVALID_UTILITY, Factory,
                                     FinancialReport, Loan, ProductionFailure,
                                     SCMLAgreement)
from negmas.apps.scml.consumers import (ConsumptionProfile,
                                        ScheduleDrivenConsumer)
from negmas.apps.scml.schedulers import (GreedyScheduler, ScheduleInfo,
                                         Scheduler)
from negmas.apps.scml.simulators import (FactorySimulator,
                                         FastFactorySimulator,
                                         storage_as_array,
                                         temporary_transaction)
from negmas.common import NamedObject
from negmas.events import Notification
from negmas.helpers import get_class
from negmas.outcomes import Issue, Outcome
from negmas.utilities import UtilityValue, normalize

from .my_mechanism import AspirationNegotiator

if True:
    from typing import (
        Dict,
        Iterable,
        Any,
        Callable,
        Collection,
        Type,
        List,
        Optional,
        Union,
    )


class MyFactoryManager(DoNothingFactoryManager):
    """My factory manager"""

    def on_production_failure(self, failures: List[ProductionFailure]) -> None:
        """
            On Production FailureCalled when there is a production failure due to lack of inputs or funds.
        """
        # for failure in failures:
        #     self.awi.logdebug(f'production failure id: {failure.line} missing_inputs: {failure.missing_inputs} \
        #                 missing_money: {failure.missing_money} missing_space: {failure.missing_space}')

        pass

    def confirm_loan(self, loan: Loan, bankrupt_if_rejected: bool) -> bool:
        # self.awi.logdebug(f'loan: {Loan}, Bankrupt_if_rejected:{bankrupt_if_rejected}')
        return bankrupt_if_rejected

    def confirm_contract_execution(self, contract: Contract) -> bool:
        # self.awi.logdebug(f'contract:{contract}')
        # import random
        # control_probability_factor = 0.1
        #  random return true confirm contract execution
        # def decision(probability):
        #     return random.random() < probability
        # if decision(control_probability_factor):
        #     return True
        # return False
        return True

    def set_renegotiation_agenda(
        self, contract: Contract, breaches: List[Breach]
    ) -> Optional[RenegotiationRequest]:
        # self.awi.logdebug(f'Contract set renegotiation agenda {contract}')
        # self.awi.logdebug(f'breaches set renegotiation agenda {breaches}')
        # total_breach_levels = defaultdict(int)
        # for breach in breaches:
        #     total_breach_levels[breach.perpetrator] += breach.level
        # for perpetrator,total_breach_level in total_breach_levels.items():
        #     : Total breach Level
        #     if total_breach_level > 0.5:
        #         return None
        #     else:
        #         self.awi.logdebug(f'return  new renegotiation request, publischer {self.id} total breach level of perpetrator {perpetrator} is {total_breach_level}')
        #         if 'cfp' in contract.annotation:
        #             renegotiationrequest = RenegotiationRequest(publisher=f'{self.id}', issues=contract.issues, annotation=contract.annotation)
        #             return renegotiationrequest
        #         return None
        return None

    def respond_to_renegotiation_request(
        self, contract: Contract, breaches: List[Breach], agenda: RenegotiationRequest
    ) -> Optional[Negotiator]:
        # total_breach_levels = defaultdict(int)
        # for breach in breaches:
        #     total_breach_levels[breach.perpetrator] += breach.level
        # for perpetrator, total_breach_level in total_breach_levels.items():
        #     if total_breach_level > 0.5:
        #         self.awi.logdebug(f'return new negotiator for renegotiation request None ')
        #         return None
        #     else:
        #         name = self.name + '*' + perpetrator
        #         self.awi.logdebug(f'return new negotiator for renegotiation request negotiator name {name} perpetrator {perpetrator} ')
        #         if 'cfp' in contract.annotation:
        #             neg = self.negotiator_type(name=name, **self.negotiator_params)
        #             neg.utility_function = normalize(self.ufun_factory(self, contract.annotation),
        #                                             outcomes=contract.annotation['cfp'].outcomes, infeasible_cutoff=0)
        #             return neg
        #         return None
        return None

    def __init__(
        self,
        log_file_name=None,
        screen_log=False,
        name=None,
        simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator,
        scheduler_type: Union[str, Type[Scheduler]] = GreedyScheduler,
        scheduler_params: Optional[Dict[str, Any]] = None,
        optimism: float = 0.0,
        negotiator_type: Union[
            str, Type[Negotiator]
        ] = "backend.src.nnegmas.my_mechanism.MyTestNegotiator",
        negotiator_params: Optional[Dict[str, Any]] = None,
        n_retrials=5,
        use_consumer=True,
        reactive=True,
        sign_only_guaranteed_contracts=False,
        riskiness=0.0,
        max_insurance_premium: float = 0.1,
    ):
        super().__init__(name=name, simulator_type=simulator_type)
        # LoggerMixin.__init__(self, file_name=log_file_name)
        self.negotiator_type = get_class(negotiator_type, scope=globals())
        self.negotiator_params = (
            negotiator_params if negotiator_params is not None else {}
        )
        self.optimism = optimism
        self.ufun_factory: Union[
            Type[NegotiatorUtility], Callable[[Any, Any], NegotiatorUtility]
        ]
        if optimism < 1e-6:
            self.ufun_factory = PessimisticNegotiatorUtility
        elif optimism > 1 - 1e-6:
            self.ufun_factory = OptimisticNegotiatorUtility
        else:
            self.ufun_factory: NegotiatorUtility = lambda agent, annotation: AveragingNegotiatorUtility(
                agent=agent, annotation=annotation, optimism=self.optimism
            )
        self.max_insurance_premium = max_insurance_premium
        self.n_retrials = n_retrials
        self.n_neg_trials: Dict[str, int] = defaultdict(int)
        self.consumer = None
        self.use_consumer = use_consumer
        self.reactive = reactive
        self.sign_only_guaranteed_contracts = sign_only_guaranteed_contracts
        self.contract_schedules: Dict[str, ScheduleInfo] = {}
        self.riskiness = riskiness
        self.negotiation_margin = int(round(n_retrials * max(0.0, 1.0 - riskiness)))
        self.scheduler_type: Type[Scheduler] = get_class(
            scheduler_type, scope=globals()
        )
        self.scheduler: Scheduler = None
        self.scheduler_params: Dict[
            str, Any
        ] = scheduler_params if scheduler_params is not None else {}

    def total_utility(self, contracts: Collection[Contract] = ()) -> float:
        """Calculates the total utility for the agent of a collection of contracts"""
        if self.scheduler is None:
            raise ValueError("Cannot calculate total utility without a scheduler")
        min_concluded_at = self.awi.current_step
        min_sign_at = min_concluded_at + self.awi.default_signing_delay
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(
                contracts=contracts,
                assume_no_further_negotiations=False,
                ensure_storage_for=self.transportation_delay,
                start_at=min_sign_at,
            )
        if not schedule.valid:
            return INVALID_UTILITY
        return schedule.final_balance

    def init(self):
        if self.use_consumer:
            # @todo add the parameters of the consumption profile as parameters of the greedy factory manager
            #  TODO:1  Initialize a greedy scheduler and a consumer agent for managing need acquisition for production
            self.consumer: ScheduleDrivenConsumer = ScheduleDrivenConsumer(
                profiles=dict(
                    zip(
                        self.consuming.keys(),
                        (
                            ConsumptionProfile(schedule=[_] * self.awi.n_steps)
                            for _ in itertools.repeat(0)
                        ),
                    )
                ),
                consumption_horizon=self.awi.n_steps,
                immediate_cfp_update=True,
                name=self.name,
            )
            # self.logdebug(f'{self.consuming}')
            self.consumer.id = self.id
            self.consumer.awi = self.awi
            self.consumer.init_()
        self.scheduler = self.scheduler_type(
            manager_id=self.id,
            awi=self.awi,
            max_insurance_premium=self.max_insurance_premium,
            **self.scheduler_params,
        )
        self.scheduler.init(
            simulator=self.simulator,
            products=self.products,
            processes=self.processes,
            producing=self.producing,
            profiles=self.compiled_profiles,
        )

    def respond_to_negotiation_request(
        self, cfp: "CFP", partner: str
    ) -> Optional[Negotiator]:
        if self.awi.is_bankrupt(partner):
            return None
        if self.use_consumer:
            return self.consumer.respond_to_negotiation_request(
                cfp=cfp, partner=partner
            )
        else:
            name = self.name + "*" + partner
            neg = self.negotiator_type(
                name=self.name + "*" + partner, **self.negotiator_params
            )
            self.awi.logdebug(f"respond to negotiation request neg name {name}")
            neg.utility_function = normalize(
                self.ufun_factory(self, self._create_annotation(cfp=cfp)),
                outcomes=cfp.outcomes,
                infeasible_cutoff=0,
            )
            return neg

    def on_negotiation_success(
        self, contract: Contract, mechanism: AgentMechanismInterface
    ):
        if self.use_consumer:
            self.consumer.on_negotiation_success(contract, mechanism)

    def on_negotiation_failure(
        self,
        partners: List[str],
        annotation: Dict[str, Any],
        mechanism: AgentMechanismInterface,
        state: MechanismState,
    ) -> None:
        # TODO8: if the factory manage was not the publisher of the cfp, and leading to this negotionation, it can retry negotiation up to 5 times per cfp with the same utility function
        if self.use_consumer:
            self.consumer.on_negotiation_failure(partners, annotation, mechanism, state)
        cfp = annotation["cfp"]
        thiscfp = self.awi.bb_query(section="cfps", query=cfp.id, query_keys=True)
        if (
            cfp.publisher != self.id
            and thiscfp is not None
            and len(thiscfp) > 0
            and self.n_neg_trials[cfp.id] < self.n_retrials
        ):
            self.awi.logdebug(f"Renegotiating {self.n_neg_trials[cfp.id]} on {cfp}")
            self.on_new_cfp(cfp=annotation["cfp"])

    def _execute_schedule(self, schedule: ScheduleInfo, contract: Contract) -> None:
        # TODO: what is exactly mean of factory simulator is not defined
        if self.simulator is None:
            raise ValueError("No factory simulator is defined")
        awi: SCMLAWI = self.awi
        total = contract.agreement["unit_price"] * contract.agreement["quantity"]
        product = contract.annotation["cfp"].product
        # TODO: For buyer use consumer
        if contract.annotation["buyer"] == self.id:
            self.simulator.buy(
                product=product,
                quantity=contract.agreement["quantity"],
                price=total,
                t=contract.agreement["time"],
            )
            if total <= 0 or self.max_insurance_premium < 0.0 or contract is None:
                return
            premium = awi.evaluate_insurance(contract=contract)
            if premium is None:
                return
            relative_premium = premium / total
            if relative_premium <= self.max_insurance_premium:
                awi.buy_insurance(contract=contract)
                self.simulator.pay(premium, self.awi.current_step)
            return
        # I am a seller
        # TODO: factory manager as seller
        self.simulator.sell(
            product=product,
            quantity=contract.agreement["quantity"],
            price=total,
            t=contract.agreement["time"],
        )
        for job in schedule.jobs:
            if job.action == "run":
                awi.schedule_job(job, contract=contract)
            elif job.action == "stop":
                awi.stop_production(
                    line=job.line,
                    step=job.time,
                    contract=contract,
                    override=job.override,
                )
            else:
                awi.schedule_job(job, contract=contract)
            self.simulator.schedule(job=job, override=False)
        for need in schedule.needs:
            if need.quantity_to_buy <= 0:
                continue
            product_id = need.product
            # self.simulator.reserve(product=product_id, quantity=need.quantity_to_buy, t=need.step)
            if self.use_consumer:
                self.consumer.profiles[product_id].schedule[
                    need.step
                ] += need.quantity_to_buy
                self.consumer.register_product_cfps(
                    p=product_id,
                    t=need.step,
                    profile=self.consumer.profiles[product_id],
                )
                continue
            product = self.products[product_id]
            if product.catalog_price is None:
                price_range = (0.0, 100.0)
            else:
                price_range = (0.5, 1.5 * product.catalog_price)
            # @todo check this. This error is raised sometimes
            if need.step < awi.current_step:
                continue
                # raise ValueError(f'need {need} at {need.step} while running at step {awi.current_step}')
            time = (
                need.step
                if self.max_storage is not None
                else (awi.current_step, need.step)
            )
            cfp = CFP(
                is_buy=True,
                publisher=self.id,
                product=product_id,
                time=time,
                unit_price=price_range,
                quantity=(1, int(1.1 * need.quantity_to_buy)),
            )
            awi.register_cfp(cfp)

    def sign_contract(self, contract: Contract):
        if any(self.awi.is_bankrupt(partner) for partner in contract.partners):
            return None
        signature = self.id
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(
                assume_no_further_negotiations=False,
                contracts=[contract],
                ensure_storage_for=self.transportation_delay,
                start_at=self.awi.current_step + 1,
            )

        if self.sign_only_guaranteed_contracts and (
            not schedule.valid or len(schedule.needs) > 1
        ):
            self.awi.logdebug(
                f"{self.name} refused to sign contract {contract.id} because it cannot be scheduled"
            )
            return None
        # if schedule.final_balance <= self.simulator.final_balance:
        #     self.awi.logdebug(f'{self.name} refused to sign contract {contract.id} because it is not expected '
        #                       f'to lead to profit')
        #     return None
        if schedule.valid:
            profit = schedule.final_balance - self.simulator.final_balance
            self.awi.logdebug(
                f"{self.name} singing contract {contract.id} expecting "
                f'{-profit if profit < 0 else profit} {"loss" if profit < 0 else "profit"}'
            )
        else:
            self.awi.logdebug(
                f"{self.name} singing contract {contract.id} expecting breach"
            )
            return None

        self.contract_schedules[contract.id] = schedule
        return signature

    def on_contract_signed(self, contract: Contract):
        if contract.annotation["buyer"] == self.id and self.use_consumer:
            self.consumer.on_contract_signed(contract)
        schedule = self.contract_schedules[contract.id]
        if schedule is not None and schedule.valid:
            self._execute_schedule(schedule=schedule, contract=contract)
        if contract.annotation["buyer"] != self.id or not self.use_consumer:
            for negotiation in self._running_negotiations.values():
                self.notify(
                    negotiation.negotiator,
                    Notification(type="ufun_modified", data=None),
                )

    def _process_buy_cfp(self, cfp: "CFP") -> None:
        # TODO5: Condition1: use the awi interface to check the bank situation of publisher, if is bankrupt, then ignore this specical cfp
        if self.awi.is_bankrupt(cfp.publisher):
            return None
        # TODO5: total insufficient funds breaches above 10,  can not except agreement, directly ignore this cfp
        # TODO5.1: what is self.simulator???
        if self.simulator is None or not self.can_expect_agreement(
            cfp=cfp, margin=self.negotiation_margin
        ):
            return
        # TODO5: Conidtion2: if the factory can not producte the  product of this cfp, then ignore this cfp
        # TODO5.1 :requires securing input products in less than one step
        if not self.can_produce(cfp=cfp):
            return
        # TODO5: satisfy all the condition, then process this buy cfp, request **negotiation**
        if self.negotiator_type == AspirationNegotiator:
            # TODO5.1: what is the mean of assume_normalized, why when use AspirationNegotiator, set this paramters to True
            neg = self.negotiator_type(
                assume_normalized=True, name=self.name + ">" + cfp.publisher
            )
        else:
            neg = self.negotiator_type(name=self.name + ">" + cfp.publisher)
        self.request_negotiation(
            negotiator=neg,
            cfp=cfp,
            ufun=normalize(
                self.ufun_factory(self, self._create_annotation(cfp=cfp)),
                outcomes=cfp.outcomes,
                infeasible_cutoff=-1500,
            ),
        )

    def _process_sell_cfp(self, cfp: "CFP"):
        if self.awi.is_bankrupt(cfp.publisher):
            return None
        # TODO6: greedy factory manager just publiches "buy" cpfs for acquiring production needs, as use conumer, then calls the internal consumer object to handle production needs acquisition
        # TODO6.1: what's the different between use conumser and internal consumer or just the same object(checked the same object, as consumer agent)
        if self.use_consumer:
            self.consumer.on_new_cfp(cfp=cfp)

    def on_new_cfp(self, cfp: "CFP") -> None:
        if not self.reactive:
            return
        # TODO4: (1). processing the buy cfps, check in the producing of factory wether has the relativ production
        # TODO4: (2). processing the sell cfps, check in the consuming of factory wether has the selection or not
        if cfp.satisfies(
            query={"is_buy": True, "products": list(self.producing.keys())}
        ):
            self._process_buy_cfp(cfp)
        if cfp.satisfies(
            query={"is_buy": False, "products": list(self.consuming.keys())}
        ):
            self._process_sell_cfp(cfp)

    def step(self):
        # TODO2:  consumer agent for managing need acquisition for production
        if self.use_consumer:
            self.consumer.step()
        if self.reactive:
            return
        # 0. remove all my CFPs
        # self.awi.bb_remove(section='cfps', query={'publisher': self})

        # respond to interesting CFPs
        # todo: should check time and sort products by interest etc
        # TODO3: respond to buy CFPS if have the buy cfps, then call the function _process_buy_cfp(cfp)
        cfps = self.awi.bb_query(
            section="cfps", query={"products": self.producing.keys(), "is_buy": True}
        )
        if cfps is None:
            return
        for cfp in cfps.values():
            self._process_buy_cfp(cfp)

    def can_produce(self, cfp: CFP, assume_no_further_negotiations=False) -> bool:
        """Whether or not we can produce the required item in time"""
        # TODO7: determinate  wether can produce the required item in time
        # TODO7.1: the product of cfp not in producing keys return can not produce
        if cfp.product not in self.producing.keys():
            return False
        # TODO7: use SCMLAgreement to check
        agreement = SCMLAgreement(
            time=cfp.max_time, unit_price=cfp.max_unit_price, quantity=cfp.min_quantity
        )
        min_concluded_at = self.awi.current_step + 1 - int(self.immediate_negotiations)
        min_sign_at = min_concluded_at + self.awi.default_signing_delay
        if cfp.max_time < min_sign_at + 1:  # 1 is minimum time to produce the product
            return False
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(
                contracts=[
                    Contract(
                        partners=[self.id, cfp.publisher],
                        agreement=agreement,
                        annotation=self._create_annotation(cfp=cfp),
                        issues=cfp.issues,
                        signed_at=min_sign_at,
                        concluded_at=min_concluded_at,
                    )
                ],
                ensure_storage_for=self.transportation_delay,
                assume_no_further_negotiations=assume_no_further_negotiations,
                start_at=min_sign_at,
            )
        return schedule.valid and self.can_secure_needs(
            schedule=schedule, step=self.awi.current_step
        )

    def can_secure_needs(self, schedule: ScheduleInfo, step: int):
        """
        Finds if it is possible in principle to arrange these needs at the given time.

        Args:
            schedule:
            step:

        Returns:

        """
        needs = schedule.needs
        if len(needs) < 1:
            return True
        for need in needs:
            if need.quantity_to_buy > 0 and need.step < step + 1 - int(
                self.immediate_negotiations
            ):  # @todo check this
                return False
        return True


class TestFactory(DoNothingFactoryManager):
    """ Test Factory For self defined negotiation negotiator"""


class NegotiatorUtility(UtilityFunction):
    """The utility function of a negotiator."""

    def __init__(
        self,
        agent: MyFactoryManager,
        annotation: Dict[str, Any],
        name: Optional[str] = None,
    ):
        if name is None:
            name = (
                agent.name
                + "*"
                + "*".join(_ for _ in annotation["partners"] if _ != agent.id)
            )
        super().__init__(name=name)
        self.agent = agent
        self.annotation = annotation

    def _contracts(self, agreements: Iterable[SCMLAgreement]) -> Collection[Contract]:
        """Converts agreements/outcomes into contracts"""
        if self.ami is None:
            raise ValueError("No annotation is stored (No mechanism info)")
        annotation = self.ami.annotation
        return [
            Contract(
                partners=annotation["partners"],
                agreement=a,
                annotation=annotation,
                issues=self.ami.issues,
            )
            for a in agreements
        ]

    def _contract(self, agreement: SCMLAgreement) -> Contract:
        """Converts an agreement/outcome into a contract"""
        annotation = self.annotation
        return Contract(
            partners=annotation["partners"],
            agreement=agreement,
            annotation=annotation,
            issues=annotation["cfp"].issues,
        )

    def _free_sale(self, agreement: SCMLAgreement) -> bool:
        return (
            self.annotation["seller"] == self.agent.id
            and agreement["unit_price"] < 1e-6
        )

    def __call__(self, outcome: Outcome) -> Optional[UtilityValue]:
        if isinstance(outcome, dict):
            return self.call(agreement=SCMLAgreement(**outcome))
        if isinstance(outcome, SCMLAgreement):
            return self.call(agreement=outcome)
        raise ValueError(f"Outcome: {outcome} cannot be converted to an SCMLAgreement")

    @abstractmethod
    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        """Called to evaluate a agreement"""

    def xml(self, issues: List[Issue]) -> str:
        return "NegotiatorUtility has not xml representation"


class PessimisticNegotiatorUtility(NegotiatorUtility):
    """The utility function of a negotiator that assumes other negotiations currently open will fail."""

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        """An offer will be a tuple of one value which in turn will be a list of contracts"""
        if self._free_sale(agreement):
            return INVALID_UTILITY
        # contracts = self.agent.contracts
        # hypothetical = list(contracts)
        # hypothetical.append(self._contract(agreement))
        hypothetical = [self._contract(agreement)]
        base_util = self.agent.simulator.final_balance
        hypothetical = self.agent.total_utility(hypothetical)
        if hypothetical < 0:
            return INVALID_UTILITY
        return hypothetical - base_util


class OptimisticNegotiatorUtility(NegotiatorUtility):
    """The utility function of a negotiator that assumes other negotiations currently open will succeed."""

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        if self._free_sale(agreement):
            return INVALID_UTILITY
        # contracts = self.agent.contracts
        # hypothetical = list(contracts)
        # hypothetical.append(self._contract(agreement))
        hypothetical = [self._contract(agreement)]
        for negotiation in self.agent.running_negotiations:  # type: ignore
            negotiator = negotiation.negotiator
            current_offer = negotiator.my_last_proposal
            if current_offer is not None:
                hypothetical.append(self._contract(current_offer))
        base_util = self.agent.simulator.final_balance
        hypothetical = self.agent.total_utility(list(hypothetical))
        if hypothetical < 0:
            return INVALID_UTILITY
        return hypothetical - base_util


class AveragingNegotiatorUtility(NegotiatorUtility):
    """A utility function that combines optimistic and pessimistic evaluators linearly using adjustable weight"""

    def __init__(
        self,
        agent: MyFactoryManager,
        annotation: Dict[str, Any],
        name: Optional[str] = None,
        optimism: float = 0.5,
    ):
        NamedObject.__init__(self=self, name=name)
        self.optimism = optimism
        self.optimistic = OptimisticNegotiatorUtility(
            agent=agent, annotation=annotation
        )
        self.pessimistic = PessimisticNegotiatorUtility(
            agent=agent, annotation=annotation
        )

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        if self._free_sale(agreement):
            return INVALID_UTILITY
        opt, pess = self.optimistic(agreement), self.pessimistic(agreement)
        if opt is None or pess is None:
            return None
        return self.optimism * opt + (1 - self.optimism) * pess
