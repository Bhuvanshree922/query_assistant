from typing import Dict
from app.query.planner import QueryPlan


class SQLGenerationError(Exception):
    pass


class SQLGenerator:


    def generate(self, plan: QueryPlan) -> str:
        if plan.canonical_id == "most_used_feature_in_initial_period":
            return self._most_used_feature_initial_period(plan)

        if plan.canonical_id == "top_dimension_by_event":
            return self._top_dimension_by_event(plan)

        if plan.canonical_id == "events_before_order":
            return self._events_before_order(plan)

        raise SQLGenerationError(
            f"Unsupported canonical_id: {plan.canonical_id}"
        )



    def _most_used_feature_initial_period(self, plan: QueryPlan) -> str:


        days = plan.time_window.value
        limit = plan.limit

        where_clauses = [
            f"ue.event_time <= u.signup_date + INTERVAL '{days} days'"
        ]

        where_clauses.extend(self._build_filters(plan.filters))

        where_sql = " AND ".join(where_clauses)

        return f"""
        SELECT
            ue.event_type,
            COUNT(DISTINCT ue.user_id) AS users
        FROM user_events ue
        JOIN users u ON ue.user_id = u.user_id
        WHERE {where_sql}
        GROUP BY ue.event_type
        ORDER BY users DESC
        LIMIT {limit};
        """

    def _top_dimension_by_event(self, plan: QueryPlan) -> str:


        dimension = plan.dimensions[0]
        event_type = plan.filters.get("event_type")
        limit = plan.limit

        if not event_type:
            raise SQLGenerationError("event_type filter is required")

        where_clauses = [
            f"ue.event_type = '{event_type}'"
        ]

        where_clauses.extend(self._build_filters(plan.filters, exclude=["event_type"]))

        where_sql = " AND ".join(where_clauses)

        return f"""
        SELECT
            u.{dimension},
            COUNT(DISTINCT ue.user_id) AS users
        FROM user_events ue
        JOIN users u ON ue.user_id = u.user_id
        WHERE {where_sql}
        GROUP BY u.{dimension}
        ORDER BY users DESC
        LIMIT {limit};
        """

    def _events_before_order(self, plan: QueryPlan) -> str:


        return """
        SELECT
            ue.event_type,
            COUNT(*) AS occurrences
        FROM user_events ue
        JOIN orders o ON ue.user_id = o.user_id
        WHERE ue.event_time < o.order_date
        GROUP BY ue.event_type
        ORDER BY occurrences DESC
        LIMIT 10;
        """



    def _build_filters(self, filters: Dict[str, str], exclude=None):
        exclude = exclude or []
        clauses = []

        for key, value in filters.items():
            if key in exclude:
                continue

            if key == "platform":
                clauses.append(f"u.platform = '{value}'")

            elif key == "country":
                clauses.append(f"u.country = '{value}'")

        return clauses
