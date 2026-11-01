"""The frontend's mock payloads must validate against the backend models (reconciliation).

`fixtures/frontend-mock-payloads.json` is a snapshot of what the frontend's MSW mock API serves
(src/mocks in haneefojay/amanah). If a model change breaks these, the contract changed: update the
frontend schemas and refresh the snapshot in the same piece of work.
"""

import json
from pathlib import Path

import pytest

from app.modules.auth import CurrentUserResponse
from app.modules.campaigns import (
    CampaignDetailResponse,
    CampaignListResponse,
    OrganisationProfileResponse,
)

PAYLOADS = json.loads(
    (Path(__file__).parent / "fixtures" / "frontend-mock-payloads.json").read_text("utf-8")
)


def test_campaign_list() -> None:
    CampaignListResponse.model_validate(PAYLOADS["campaignList"])


@pytest.mark.parametrize("payload", PAYLOADS["campaignDetails"])
def test_campaign_details(payload: dict[str, object]) -> None:
    CampaignDetailResponse.model_validate(payload)


@pytest.mark.parametrize("payload", PAYLOADS["organisationProfiles"])
def test_organisation_profiles(payload: dict[str, object]) -> None:
    OrganisationProfileResponse.model_validate(payload)


@pytest.mark.parametrize("payload", PAYLOADS["currentUsers"])
def test_current_users(payload: dict[str, object]) -> None:
    CurrentUserResponse.model_validate(payload)


def test_round_trip_keeps_camel_case_keys() -> None:
    model = CampaignListResponse.model_validate(PAYLOADS["campaignList"])
    dumped = model.model_dump(by_alias=True, mode="json")
    assert dumped["data"][0]["targetAmount"] == PAYLOADS["campaignList"]["data"][0]["targetAmount"]
