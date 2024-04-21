# TODO: error on POSt when rule with  source / dest fields exist


class SyncRuleSide:
    pass


class SyncRule:
    source: SyncRuleSide
    destination: SyncRuleSide
    condition: Optional[SyncCondition]
