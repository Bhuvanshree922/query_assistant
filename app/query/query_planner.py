from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class TimeWindow:
    type: str 
    unit: str
    value: int

@dataclass
class resolvedQuery:
    intent: str
    subject: str
    metric: str
    dimensions: List[str]
    time_window: Optional[TimeWindow]
    filters: Optional[Dict[str, str]]

@dataclass
class QueryPlan:
    canonical_id: str
    metric: str
    dimensions: List[str]
    time_window: Optional[TimeWindow]
    filters: Optional[Dict[str, str]]
    limit: Optional[int]


    
    
    
class QueryPlanner:
    
    def plan(self, rq) -> Optional[QueryPlan]:
        
        if rq.intent == "causal":
            return None

        if self._match_most_used_feature_initial_period(rq):
            return QueryPlan(
                canonical_id="most_used_feature_in_initial_period",
                metric=rq.metric,
                dimensions=["event_type"],
                time_window=rq.time_window,
                filters=rq.filters,
                limit=5
            )

        if self._match_top_dimension_by_event(rq):
            return QueryPlan(
                canonical_id="top_dimension_by_event",
                metric=rq.metric,
                dimensions=rq.dimensions,
                time_window=rq.time_window,
                filters=rq.filters,
                limit=5
            )

        if self._match_events_before_order(rq):
            return QueryPlan(
                canonical_id="events_before_order",
                metric="count",
                dimensions=["event_type"],
                time_window=None,
                filters=rq.filters,
                limit=10
            )

        return None
    def _match_most_used_feature_initial_period(self, rq) -> bool:
        if rq.intent not in ["descriptive", "comparative"]:
            return False

        if rq.subject != "event_usage":
            return False

        if "event_type" not in rq.dimensions:
            return False

        if not rq.time_window:
            return False

        if rq.time_window.type != "initial_period":
            return False

        if rq.time_window.unit != "days":
            return False

       
        if not (1 <= rq.time_window.value <= 7):
            return False

        return True

    def _match_top_dimension_by_event(self, rq) -> bool:
        if rq.intent != "comparative":
            return False

        if rq.subject not in ["event_usage", "purchases"]:
            return False

        if not any(dim in rq.dimensions for dim in ["country", "category", "platform"]):
            return False

        if "event_type" not in rq.filters:
            return False

        return True

    def _match_events_before_order(self, rq) -> bool:
        if rq.intent != "descriptive":
            return False

        if rq.subject != "pre_purchase_behavior":
            return False

        return True
        