import json
from opentrons import protocol_api, types

metadata = {
    "created": "2026-05-26T03:06:09.981Z",
    "internalAppBuildDate": "Tue, 05 May 2026 15:37:27 GMT",
    "lastModified": "2026-05-26T03:20:15.221Z",
    "protocolDesigner": "8.10.1",
    "source": "Protocol Designer",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.28"}

def run(protocol: protocol_api.ProtocolContext) -> None:
    # Load Labware:
    well_plate_1 = protocol.load_labware(
        "corning_24_wellplate_3.4ml_flat",
        location="2",
        namespace="opentrons",
        version=5,
    )
    reservoir_1 = protocol.load_labware(
        "opentrons_tough_1_reservoir_300ml",
        location="3",
        namespace="opentrons",
        version=2,
    )

    # Load Pipettes:
    pipette_left = protocol.load_instrument("p1000_single_gen2", "left")
    pipette_right = protocol.load_instrument("p1000_single_gen2", "right")

    # Define Liquids:
    liquid_1 = protocol.define_liquid(
        "Wash",
        display_color="#b925ff",
    )
    liquid_2 = protocol.define_liquid(
        "Deprotect",
        display_color="#ffd600",
    )
    liquid_3 = protocol.define_liquid(
        "Base",
        display_color="#9dffd8",
    )
    liquid_4 = protocol.define_liquid(
        "Adenine",
        display_color="#ff9900",
    )
    liquid_5 = protocol.define_liquid(
        "Cytosine",
        display_color="#50d5ff",
    )
    liquid_6 = protocol.define_liquid(
        "Guanine",
        display_color="#ff80f5",
    )
    liquid_7 = protocol.define_liquid(
        "Thyamine",
        display_color="#7eff42",
    )
    liquid_8 = protocol.define_liquid(
        "OH Wash",
        display_color="#ff4f4f",
    )
    liquid_9 = protocol.define_liquid(
        "Column",
        display_color="#b925ff",
    )

    # Load Liquids:
    well_plate_1.load_liquid(
        wells=["A1"],
        liquid=liquid_4,
        volume=10,
    )
    well_plate_1.load_liquid(
        wells=["A2"],
        liquid=liquid_5,
        volume=10,
    )
    well_plate_1.load_liquid(
        wells=["A3"],
        liquid=liquid_6,
        volume=10,
    )
    well_plate_1.load_liquid(
        wells=["A4"],
        liquid=liquid_7,
        volume=10,
    )
    well_plate_1.load_liquid(
        wells=["B1"],
        liquid=liquid_3,
        volume=10,
    )

    # PROTOCOL STEPS



DESIGNER_APPLICATION = """{"robot":{"model":"OT-2 Standard"},"designerApplication":{"name":"opentrons/protocol-designer","version":"8.10.0","data":{"pipetteTiprackAssignments":{"f674c648-095d-46a7-a361-38bb2cdeda1c":["opentrons/opentrons_96_tiprack_1000ul/1"],"d151d046-e094-49e2-87a6-878767c9bcfc":["opentrons/opentrons_96_tiprack_1000ul/1"]},"dismissedWarnings":{"form":[],"timeline":[]},"ingredients":{"0":{"displayName":"Wash","displayColor":"#b925ff","description":null,"liquidGroupId":"0"},"1":{"displayName":"Deprotect","displayColor":"#ffd600","description":null,"liquidGroupId":"1"},"2":{"displayName":"Base","displayColor":"#9dffd8","description":null,"liquidGroupId":"2"},"3":{"displayName":"Adenine","displayColor":"#ff9900","description":null,"liquidGroupId":"3"},"4":{"displayName":"Cytosine","displayColor":"#50d5ff","description":null,"liquidGroupId":"4"},"5":{"displayName":"Guanine","displayColor":"#ff80f5","description":null,"liquidGroupId":"5"},"6":{"displayName":"Thyamine","displayColor":"#7eff42","description":null,"liquidGroupId":"6"},"7":{"displayName":"OH Wash","displayColor":"#ff4f4f","description":null,"liquidGroupId":"7"},"8":{"displayName":"Column","displayColor":"#b925ff","description":null,"liquidGroupId":"8"}},"ingredLocations":{"af9d5f70-156e-47bf-b9f4-1efb0c160c78:opentrons/corning_24_wellplate_3.4ml_flat/5":{"A1":{"3":{"volume":10}},"A2":{"4":{"volume":10}},"A3":{"5":{"volume":10}},"A4":{"6":{"volume":10}},"B1":{"2":{"volume":10}}}},"savedStepForms":{"__INITIAL_DECK_SETUP_STEP__":{"stepType":"manualIntervention","id":"__INITIAL_DECK_SETUP_STEP__","labwareLocationUpdate":{"af9d5f70-156e-47bf-b9f4-1efb0c160c78:opentrons/corning_24_wellplate_3.4ml_flat/5":"2","6e49b46d-9d86-44ba-ae09-1dd69b646647:opentrons/opentrons_tough_1_reservoir_300ml/2":"3"},"pipetteLocationUpdate":{"f674c648-095d-46a7-a361-38bb2cdeda1c":"left","d151d046-e094-49e2-87a6-878767c9bcfc":"right"},"moduleLocationUpdate":{},"moduleStateUpdate":{},"trashBinLocationUpdate":{"0706c5de-dc8e-47d8-8931-c0ab9fc0fb44:trashBin":"cutout12"},"wasteChuteLocationUpdate":{},"stagingAreaLocationUpdate":{},"gripperLocationUpdate":{}}},"orderedStepIds":[],"pipettes":{"f674c648-095d-46a7-a361-38bb2cdeda1c":{"pipetteName":"p1000_single_gen2"},"d151d046-e094-49e2-87a6-878767c9bcfc":{"pipetteName":"p1000_single_gen2"}},"modules":{},"labware":{"af9d5f70-156e-47bf-b9f4-1efb0c160c78:opentrons/corning_24_wellplate_3.4ml_flat/5":{"displayName":"Corning 24 Well Plate 3.4 mL Flat","labwareDefURI":"opentrons/corning_24_wellplate_3.4ml_flat/5"},"6e49b46d-9d86-44ba-ae09-1dd69b646647:opentrons/opentrons_tough_1_reservoir_300ml/2":{"displayName":"Opentrons Tough 300 mL 1 Well Reservoir","labwareDefURI":"opentrons/opentrons_tough_1_reservoir_300ml/2"}}}},"metadata":{"protocolName":"","author":"","description":"","source":"Protocol Designer","created":1779764769981,"lastModified":1779765615221}}"""
