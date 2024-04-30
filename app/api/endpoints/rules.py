# TODO: error on POSt when rule with  source / dest fields exist


from fastapi import APIRouter
from app.core.db import DocumentDatabase
from app.core.logger import logger
from app.core.providers import Provider, get_provider
from app.core.rule import Rule, RuleDTO
from fastapi import Depends, FastAPI, HTTPException
from app.core.db import get_db
import app.services.rules as rules

import typing as t

router = APIRouter()


# project id reserved for specific trackers which might
# have differnet fields per project
@router.get("/api/rule_list")
def get_rules(db: DocumentDatabase = Depends(get_db)):
    return rules.get_rules(db)


@router.post("/api/add_rule")
def add_rule(rule: RuleDTO, db: DocumentDatabase = Depends(get_db)):
    return rules.add_rule(Rule.from_dto(rule), db)


@router.get("/api/remove_rule")
def remove_rule(rule: RuleDTO, db: DocumentDatabase = Depends(get_db)):
    return rules.remove_rule(Rule.from_dto(rule), db)
