class SQLValidationError(Exception):
    pass
class SQLValidator:
    
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "create"]
    FORBIDDEN_COLUMNS = [
        "email",
        "phone",
        "password",
        "address",
    ]
    def validate(self, sql: str):
        self._validate_select_clause(sql)
        self._validate_limit_availability(sql)
        self._validate_keywords(sql)
        self._check_forbidden_columns(sql)
    
    def _validate_select_clause(self,sql):
        if not sql.strip().lower().startswith("select"):
            raise SQLValidationError("Only SELECT statements are allowed.")
    def _validate_limit_availability(self,sql):
        if "limit" not in sql.lower():
            raise SQLValidationError("Only queries with LIMIT clause are allowed.")
    def _validate_keywords(self,sql):
        forbidden_keywords = self.forbidden_keywords
        for keyword in forbidden_keywords:
            if keyword in sql.lower():
                raise SQLValidationError(f"Keyword '{keyword}' is not allowed.")
    def _check_forbidden_columns(self,sql):
        forbidden_columns = self.FORBIDDEN_COLUMNS
        for column in forbidden_columns:
            if column in sql.lower():
                raise SQLValidationError(f"Column '{column}' is not allowed.")



