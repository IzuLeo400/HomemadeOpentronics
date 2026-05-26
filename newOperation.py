import json
from opentrons import protocol_api, types

metadata = {
    "protocolName": "Daniels Playground",
    "created": "2022-07-05T17:18:47.138Z",
    "internalAppBuildDate": "Tue, 05 May 2026 15:37:27 GMT",
    "lastModified": "2026-05-26T02:53:11.253Z",
    "protocolDesigner": "8.10.1",
    "source": "Protocol Designer",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.28"}

properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 3},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},



def run(protocol: protocol_api.ProtocolContext) -> None:
    # Load Labware:
    tip_rack = protocol.load_labware(
        "opentrons_96_tiprack_1000ul",
        location="7",
        label="Opentrons 96 Tip Rack 1000 µL",
        namespace="opentrons",
        version=1,
    )
    reservoir_wash = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/danny_1_reservoir_350000ul/1"],
        location="1",
        label="Wash",
    )
    reservoir_24 = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/dan_24_reservoir_4000ul/1"],
        location="2",
    )
    reservoir_OH = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/danny_1_reservoir_350000ul/1"],
        location="3",
        label="WashOH",
    )
    reservoir_deprotect = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/danny_1_reservoir_350000ul/1"],
        location="8",
        label="Deprotect",
    )
    column_holder = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/columnholder_5_wellplate_100000ul/1"],
        location="4",
    )

    # Load Pipettes:
    pipette_left = protocol.load_instrument("p1000_single_gen2", "left")
    pipette_right = protocol.load_instrument("p1000_single_gen2", "right")

    # Define Liquids:
    Wash = protocol.define_liquid(
        "Wash",
        display_color="#b925ff",
    )
    Deprotect = protocol.define_liquid(
        "Deprotect",
        display_color="#ffd600",
    )
    WashOH = protocol.define_liquid(
        "WashOH",
        display_color="#9dffd8",
    )
    Base = protocol.define_liquid(
        "Base",
        display_color="#ff9900",
    )
    A = protocol.define_liquid(
        "A",
        display_color="#50d5ff",
    )
    T = protocol.define_liquid(
        "T",
        display_color="#299214",
    )
    G = protocol.define_liquid(
        "G",
        display_color="#2101d6",
    )
    C = protocol.define_liquid(
        "C",
        display_color="#ff5050",
    )

    # Load Liquids:
    reservoir_wash.load_liquid(
        wells=["A1"],
        liquid=Wash,
        volume=350000,
    )
    reservoir_deprotect.load_liquid(
        wells=["A1"],
        liquid=Deprotect,
        volume=50000,
    )
    reservoir_OH.load_liquid(
        wells=["A1"],
        liquid=WashOH,
        volume=50000,
    )
    reservoir_24.load_liquid(
        wells=["A3"],
        liquid=Base,
        volume=4000,
    )
    reservoir_24.load_liquid(
        wells=["A1"],
        liquid=A,
        volume=4000,
    )
    reservoir_24.load_liquid(
        wells=["B1"],
        liquid=T,
        volume=4000,
    )
    reservoir_24.load_liquid(
        wells=["C1"],
        liquid=G,
        volume=4000,
    )
    reservoir_24.load_liquid(
        wells=["D1"],
        liquid=C,
        volume=4000,
    )

    #Tip rack organization: 0 = A, 1 = T, 2 = G, 3 = C, 
    # 4 = Wash, 5 = WashOH, 6 = Deprotect
    # 7 = A Mix, 8 = T Mix, 9 = G Mix, 10 = C Mix
    # 11 = Base
    TipRackOrganization = {
        "A": 0, "T": 1, "G": 2, "C": 3, "Wash": 4, "WashOH": 5, "Deprotect": 6, 
        "A_Mix": 7, "T_Mix": 8, "G_Mix": 9, "C_Mix": 10, "Base": 11
    }
    Source = {
        "A": reservoir_24["A1"], "T": reservoir_24["B1"], "G": reservoir_24["C1"], "C": reservoir_24["D1"], 
        "Wash": reservoir_wash["A1"], "WashOH": reservoir_OH["A1"], "Deprotect": reservoir_deprotect["A1"], 
        "Base": reservoir_24["A3"]
    }
    Dest = {
        "A": reservoir_24["A2"], "T": reservoir_24["B2"], "G": reservoir_24["C2"], "C": reservoir_24["D2"]
    }
    def transfer(Liquid, Volume, Destination=None, Name="Untitled") -> None:
        pipette_left.pick_up_tip(tip_rack.wells()[TipRackOrganization[Liquid]])
        pipette_left.transfer_with_liquid_class(
            volume=Volume,
            source=[Source[Liquid]],
            dest=[Dest[Liquid] if Destination==None else Destination],
            new_tip="never",
            trash_location=protocol.fixed_trash,
            keep_last_tip=True,
            tip_racks=[tip_rack],
            liquid_class=protocol.define_liquid_class(
                name=Name,
                properties=properties
            ),
        )
        pipette_left.return_tip()
    
    # PROTOCOL STEPS
    transfer("Wash", 1000, column_holder["A1"], "ColumnHolderWash1")
    transfer("Wash", 1000, column_holder["A1"], "ColumnHolderWash2")
    transfer("C", 120, Name="Monomer C -> mix C")
    transfer("Base", 30, Dest["C"])
    

    # Step 3: wash pause
    #protocol.delay(seconds=120, msg="wash pause")

    # Step 2: Monomer C -> mix C
    pipette_left.transfer_with_liquid_class(
        volume=120,
        source=[reservoir_24["B1"]],
        dest=[reservoir_24["B2"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="Monomer C -> mix C",
            properties=properties
        ),
    )
    pipette_left.drop_tip()

    pipette_right.transfer_with_liquid_class(
        volume=30,
        source=[reservoir_24["A1"]],
        dest=[reservoir_24["B2"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="Base -> Mix C",
            properties=properties
        ),
    )


    # Step 6: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_6",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 7: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_7",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 8: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 9: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_9",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 10: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_10",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 11: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 12: Ahx Deprotection 1
    pipette_left.transfer_with_liquid_class(
        volume=450,
        source=[reservoir_2["A1"], reservoir_2["A1"], reservoir_2["A1"], reservoir_2["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_12",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 4},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 13: Ahx deprotection 1 pause
    protocol.delay(seconds=300, msg="Ahx deprotection 1 pause")

    # Step 14: Ahx Deprotection 2
    pipette_left.transfer_with_liquid_class(
        volume=450,
        source=[reservoir_2["A1"], reservoir_2["A1"], reservoir_2["A1"], reservoir_2["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_14",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 4},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 15: Ahx deprotection 1 pause
    protocol.delay(seconds=300, msg="Ahx deprotection 1 pause")

    # Step 16: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_16",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 17: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_17",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 18: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 19: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_19",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 20: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_20",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 21: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 22: CL addition
    pipette_left.transfer_with_liquid_class(
        volume=300,
        source=[reservoir_2["A3"], reservoir_2["A3"], reservoir_2["A3"], reservoir_2["A3"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_22",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 3},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 23: CL pause
    protocol.delay(seconds=10800, msg="CL pause")

    # Step 24: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_24",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 25: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_25",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 26: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 27: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_27",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 28: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_28",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 29: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 30: Ahx Deprotection 1
    pipette_left.transfer_with_liquid_class(
        volume=450,
        source=[reservoir_2["B1"], reservoir_2["B1"], reservoir_2["B1"], reservoir_2["B1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_30",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 4},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 31: Ahx deprotection 1 pause
    protocol.delay(seconds=300, msg="Ahx deprotection 1 pause")

    # Step 32: Ahx Deprotection 2
    pipette_left.transfer_with_liquid_class(
        volume=450,
        source=[reservoir_2["B1"], reservoir_2["B1"], reservoir_2["B1"], reservoir_2["B1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_32",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 4},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 33: Ahx deprotection 1 pause
    protocol.delay(seconds=300, msg="Ahx deprotection 1 pause")

    # Step 34: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_34",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 35: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_35",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 36: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 37: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_37",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 38: DMI wash
    pipette_left.transfer_with_liquid_class(
        volume=1000,
        source=[reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"], reservoir_1["A1"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_38",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 39: wash pause
    protocol.delay(seconds=120, msg="wash pause")

    # Step 40: Vivo Addition
    pipette_left.transfer_with_liquid_class(
        volume=300,
        source=[reservoir_2["A4"], reservoir_2["A4"], reservoir_2["A4"], reservoir_2["A4"]],
        dest=[well_plate_1["A1"], well_plate_1["A2"], well_plate_1["A3"], well_plate_1["A4"]],
        new_tip="once",
        trash_location=protocol.fixed_trash,
        keep_last_tip=True,
        tip_racks=[tip_rack],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_40",
            properties={"p1000_single_gen2": {"opentrons/opentrons_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 4},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 60},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 274.7)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 125,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 125,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 0)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

CUSTOM_LABWARE = json.loads("""{"custom_beta/danny_1_reservoir_350000ul/1":{"ordering":[["A1"]],"brand":{"brand":"Danny","brandId":["Danny'sStuff"]},"metadata":{"displayName":"Danny 1 Reservoir 350000 µL","displayCategory":"reservoir","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.5,"yDimension":85.4,"zDimension":110},"wells":{"A1":{"depth":106,"totalLiquidVolume":350000,"shape":"circular","diameter":80,"x":63.75,"y":42.7,"z":4}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1"]}],"parameters":{"format":"irregular","quirks":["centerMultichannelOnWells","touchTipDisabled"],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"danny_1_reservoir_350000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}},"custom_beta/dan_24_reservoir_4000ul/1":{"ordering":[["A1","B1","C1","D1"],["A2","B2","C2","D2"],["A3","B3","C3","D3"],["A4","B4","C4","D4"],["A5","B5","C5","D5"],["A6","B6","C6","D6"]],"brand":{"brand":"Dan","brandId":["Dan2"]},"metadata":{"displayName":"Dan 24 Reservoir 4000 µL","displayCategory":"reservoir","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.47,"zDimension":46},"wells":{"A1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":72.17,"z":2},"B1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":52.67,"z":2},"C1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":33.17,"z":2},"D1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":13.67,"z":2},"A2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":72.17,"z":2},"B2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":52.67,"z":2},"C2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":33.17,"z":2},"D2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":13.67,"z":2},"A3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":72.17,"z":2},"B3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":52.67,"z":2},"C3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":33.17,"z":2},"D3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":13.67,"z":2},"A4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":72.17,"z":2},"B4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":52.67,"z":2},"C4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":33.17,"z":2},"D4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":13.67,"z":2},"A5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":72.17,"z":2},"B5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":52.67,"z":2},"C5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":33.17,"z":2},"D5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":13.67,"z":2},"A6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":72.17,"z":2},"B6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":52.67,"z":2},"C6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":33.17,"z":2},"D6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":13.67,"z":2}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1","B1","C1","D1","A2","B2","C2","D2","A3","B3","C3","D3","A4","B4","C4","D4","A5","B5","C5","D5","A6","B6","C6","D6"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"dan_24_reservoir_4000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}},"custom_beta/columnholder_5_wellplate_100000ul/1":{"ordering":[["A1"],["A2"],["A3"],["A4"],["A5"]],"brand":{"brand":"ColumnHolder","brandId":["DanYijia"]},"metadata":{"displayName":"ColumnHolder 5 Well Plate 100000 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":87},"wells":{"A1":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":19.8,"y":42.74,"z":42},"A2":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":41.8,"y":42.74,"z":42},"A3":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":63.8,"y":42.74,"z":42},"A4":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":85.8,"y":42.74,"z":42},"A5":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":107.8,"y":42.74,"z":42}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1","A2","A3","A4","A5"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"columnholder_5_wellplate_100000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")

DESIGNER_APPLICATION = """{"robot":{"model":"OT-2 Standard"},"designerApplication":{"name":"opentrons/protocol-designer","version":"8.10.0","data":{"pipetteTiprackAssignments":{"878c5160-fc86-11ec-9d9e-4b22ad198770":["opentrons/opentrons_96_tiprack_1000ul/1"],"878c5161-fc86-11ec-9d9e-4b22ad198770":["opentrons/opentrons_96_tiprack_1000ul/1"]},"dismissedWarnings":{"form":[],"timeline":["ASPIRATE_MORE_THAN_WELL_CONTENTS"]},"ingredients":{"0":{"displayName":"DMI","description":null,"liquidGroupId":"0","displayColor":"#b925ff","liquidClass":null},"1":{"displayName":"Deprotection","description":null,"liquidGroupId":"1","displayColor":"#ffd600","liquidClass":null},"2":{"displayName":"Ahx","description":null,"liquidGroupId":"2","displayColor":"#9dffd8","liquidClass":null},"3":{"displayName":"CL","description":null,"liquidGroupId":"3","displayColor":"#ff9900","liquidClass":null},"4":{"displayName":"Vivo","description":null,"liquidGroupId":"4","displayColor":"#50d5ff","liquidClass":null}},"ingredLocations":{"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1":{"A1":{"0":{"volume":350000}}},"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1":{"A1":{"1":{"volume":4000}},"B1":{"1":{"volume":4000}},"C1":{"1":{"volume":4000}},"A2":{"2":{"volume":2000}},"A3":{"3":{"volume":2000}},"A4":{"4":{"volume":2000}}}},"savedStepForms":{"__INITIAL_DECK_SETUP_STEP__":{"labwareLocationUpdate":{"878db0f0-fc86-11ec-9d9e-4b22ad198770:opentrons/opentrons_96_tiprack_1000ul/1":"1","84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1":"2","cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1":"3","22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1":"7"},"pipetteLocationUpdate":{"878c5160-fc86-11ec-9d9e-4b22ad198770":"left","878c5161-fc86-11ec-9d9e-4b22ad198770":"right"},"moduleLocationUpdate":{},"stepType":"manualIntervention","id":"__INITIAL_DECK_SETUP_STEP__","stagingAreaLocationUpdate":{},"gripperLocationUpdate":{},"wasteChuteLocationUpdate":{},"trashBinLocationUpdate":{"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin":"cutout12"},"moduleStateUpdate":{}},"84cb4ab0-fc88-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"84cb4ab0-fc88-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"877cd620-fc88-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"877cd620-fc88-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"0bd6a0c0-fcb8-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"0bd6a0c0-fcb8-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"dffe4ea0-fc88-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":3,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"300","stepType":"moveLiquid","stepName":"Ahx addition","stepDetails":"","id":"dffe4ea0-fc88-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"ef1bc890-fc88-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"Ahx pause","pauseTemperature":null,"pauseTime":"03:00:00","id":"ef1bc890-fc88-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"Ahx pause","stepDetails":""},"50119a20-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"50119a20-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"5eb63a90-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"5eb63a90-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"c786f9a0-fcb3-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"c786f9a0-fcb3-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"5e262f90-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"5e262f90-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"5d877e90-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"5d877e90-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"19678740-fcb8-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"19678740-fcb8-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"5d60d930-fc89-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":4,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"450","stepType":"moveLiquid","stepName":"Ahx Deprotection 1","stepDetails":"","id":"5d60d930-fc89-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"6b9f16b0-fc89-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"Ahx deprotection 1 pause","pauseTemperature":null,"pauseTime":"00:05:00","id":"6b9f16b0-fc89-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"Ahx deprotection 1 pause","stepDetails":""},"8b4ad8a0-fc89-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":4,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"450","stepType":"moveLiquid","stepName":"Ahx Deprotection 2","stepDetails":"","id":"8b4ad8a0-fc89-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"ce8f4e20-fc89-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"Ahx deprotection 1 pause","pauseTemperature":null,"pauseTime":"00:05:00","id":"ce8f4e20-fc89-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"Ahx deprotection 1 pause","stepDetails":""},"82e00a90-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"82e00a90-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"96434480-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"96434480-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"96947520-fcb3-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"96947520-fcb3-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"9453a980-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"9453a980-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"97ff9a80-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"97ff9a80-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"264152c0-fcb8-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"264152c0-fcb8-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"c5610900-fc8a-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":3,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A3"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"300","stepType":"moveLiquid","stepName":"CL addition","stepDetails":"","id":"c5610900-fc8a-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"ce4cdc00-fc8b-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"CL pause","pauseTemperature":null,"pauseTime":"03:00:00","id":"ce4cdc00-fc8b-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"CL pause","stepDetails":""},"f7d61960-fc8b-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"f7d61960-fc8b-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"3972ab40-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"3972ab40-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"60f27250-fcb3-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"60f27250-fcb3-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"3723d940-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"3723d940-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"356ed640-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"356ed640-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"2f5a6cc0-fcb8-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"2f5a6cc0-fcb8-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"833a4da0-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":4,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["B1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"450","stepType":"moveLiquid","stepName":"Ahx Deprotection 1","stepDetails":"","id":"833a4da0-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"833a4da1-fc8c-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"Ahx deprotection 1 pause","pauseTemperature":null,"pauseTime":"00:05:00","id":"833a4da1-fc8c-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"Ahx deprotection 1 pause","stepDetails":""},"833a4da2-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":4,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["B1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"450","stepType":"moveLiquid","stepName":"Ahx Deprotection 2","stepDetails":"","id":"833a4da2-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"833a4da3-fc8c-11ec-9d9e-4b22ad198770":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"Ahx deprotection 1 pause","pauseTemperature":null,"pauseTime":"00:05:00","id":"833a4da3-fc8c-11ec-9d9e-4b22ad198770","stepType":"pause","stepName":"Ahx deprotection 1 pause","stepDetails":""},"833a4da7-fc8c-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"833a4da7-fc8c-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"382f8770-fc8d-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"382f8770-fc8d-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"5428ac60-fcb3-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"5428ac60-fcb3-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"356df670-fc8d-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"356df670-fc8d-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"2f08fff0-fc8d-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"1000","stepType":"moveLiquid","stepName":"DMI wash","stepDetails":"","id":"2f08fff0-fc8d-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null},"362fb140-fcb8-11ec-b7a8-2ba1dd32dea3":{"moduleId":null,"pauseAction":"untilTime","pauseMessage":"wash pause","pauseTemperature":null,"pauseTime":"00:02:00","id":"362fb140-fcb8-11ec-b7a8-2ba1dd32dea3","stepType":"pause","stepName":"wash pause","stepDetails":""},"71c9aa00-fc8e-11ec-9d9e-4b22ad198770":{"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"100","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":274.7,"aspirate_labware":"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":4,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":0,"aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":125,"aspirate_retract_x_position":null,"aspirate_retract_y_position":null,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":0,"aspirate_submerge_speed":125,"aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":null,"aspirate_submerge_y_position":null,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":400,"aspirate_touchTip_mmFromEdge":0,"aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A4"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":274.7,"blowout_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","blowout_mmFromBottom":null,"blowout_x_position":null,"blowout_y_position":null,"blowout_position_reference":"well-top","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":null,"dispense_airGap_checkbox":false,"dispense_airGap_volume":"100","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":274.7,"dispense_labware":"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1","dispense_mix_checkbox":false,"dispense_mix_times":null,"dispense_mix_volume":null,"dispense_mmFromBottom":60,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":0,"dispense_retract_mmFromBottom":2,"dispense_retract_speed":125,"dispense_retract_x_position":null,"dispense_retract_y_position":null,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":0,"dispense_submerge_speed":125,"dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":null,"dispense_submerge_y_position":null,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":null,"dispense_touchTip_speed":400,"dispense_touchTip_mmFromEdge":0,"dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","A2","A3","A4"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":"100","dropTip_location":"1f453aac-e69e-48ff-b1f5-f5e20fd998dd:trashBin","liquidClassesSupported":false,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"878c5160-fc86-11ec-9d9e-4b22ad198770","preWetTip":false,"primaryNozzle":"A1","pushOut_checkbox":false,"pushOut_volume":0,"tipRack":"opentrons/opentrons_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"300","stepType":"moveLiquid","stepName":"Vivo Addition","stepDetails":"","id":"71c9aa00-fc8e-11ec-9d9e-4b22ad198770","dispense_touchTip_mmfromTop":null}},"orderedStepIds":["84cb4ab0-fc88-11ec-9d9e-4b22ad198770","877cd620-fc88-11ec-9d9e-4b22ad198770","0bd6a0c0-fcb8-11ec-b7a8-2ba1dd32dea3","dffe4ea0-fc88-11ec-9d9e-4b22ad198770","ef1bc890-fc88-11ec-9d9e-4b22ad198770","50119a20-fc8a-11ec-9d9e-4b22ad198770","5eb63a90-fc8a-11ec-9d9e-4b22ad198770","c786f9a0-fcb3-11ec-b7a8-2ba1dd32dea3","5e262f90-fc8a-11ec-9d9e-4b22ad198770","5d877e90-fc8a-11ec-9d9e-4b22ad198770","19678740-fcb8-11ec-b7a8-2ba1dd32dea3","5d60d930-fc89-11ec-9d9e-4b22ad198770","6b9f16b0-fc89-11ec-9d9e-4b22ad198770","8b4ad8a0-fc89-11ec-9d9e-4b22ad198770","ce8f4e20-fc89-11ec-9d9e-4b22ad198770","82e00a90-fc8a-11ec-9d9e-4b22ad198770","96434480-fc8a-11ec-9d9e-4b22ad198770","96947520-fcb3-11ec-b7a8-2ba1dd32dea3","9453a980-fc8a-11ec-9d9e-4b22ad198770","97ff9a80-fc8a-11ec-9d9e-4b22ad198770","264152c0-fcb8-11ec-b7a8-2ba1dd32dea3","c5610900-fc8a-11ec-9d9e-4b22ad198770","ce4cdc00-fc8b-11ec-9d9e-4b22ad198770","f7d61960-fc8b-11ec-9d9e-4b22ad198770","3972ab40-fc8c-11ec-9d9e-4b22ad198770","60f27250-fcb3-11ec-b7a8-2ba1dd32dea3","3723d940-fc8c-11ec-9d9e-4b22ad198770","356ed640-fc8c-11ec-9d9e-4b22ad198770","2f5a6cc0-fcb8-11ec-b7a8-2ba1dd32dea3","833a4da0-fc8c-11ec-9d9e-4b22ad198770","833a4da1-fc8c-11ec-9d9e-4b22ad198770","833a4da2-fc8c-11ec-9d9e-4b22ad198770","833a4da3-fc8c-11ec-9d9e-4b22ad198770","833a4da7-fc8c-11ec-9d9e-4b22ad198770","382f8770-fc8d-11ec-9d9e-4b22ad198770","5428ac60-fcb3-11ec-b7a8-2ba1dd32dea3","356df670-fc8d-11ec-9d9e-4b22ad198770","2f08fff0-fc8d-11ec-9d9e-4b22ad198770","362fb140-fcb8-11ec-b7a8-2ba1dd32dea3","71c9aa00-fc8e-11ec-9d9e-4b22ad198770"],"pipettes":{"878c5160-fc86-11ec-9d9e-4b22ad198770":{"pipetteName":"p1000_single_gen2"},"878c5161-fc86-11ec-9d9e-4b22ad198770":{"pipetteName":"p1000_single_gen2"}},"modules":{},"labware":{"878db0f0-fc86-11ec-9d9e-4b22ad198770:opentrons/opentrons_96_tiprack_1000ul/1":{"displayName":"Opentrons 96 Tip Rack 1000 µL","labwareDefURI":"opentrons/opentrons_96_tiprack_1000ul/1"},"84f00630-fc87-11ec-9d9e-4b22ad198770:custom_beta/danny_1_reservoir_350000ul/1":{"displayName":"DMI","labwareDefURI":"custom_beta/danny_1_reservoir_350000ul/1"},"cac8e230-fc87-11ec-9d9e-4b22ad198770:custom_beta/dan_24_reservoir_4000ul/1":{"displayName":"Dan 24 Reservoir 4000 µL","labwareDefURI":"custom_beta/dan_24_reservoir_4000ul/1"},"22155d20-fc88-11ec-9d9e-4b22ad198770:custom_beta/columnholder_5_wellplate_100000ul/1":{"displayName":"ColumnHolder 5 Well Plate 100000 µL","labwareDefURI":"custom_beta/columnholder_5_wellplate_100000ul/1"}}}},"metadata":{"protocolName":"4 K columns Ahx, CL, Vivo addition","author":"","description":"","created":1657041527138,"lastModified":1779763991253,"category":null,"subcategory":null,"tags":[],"source":"Protocol Designer"}}"""