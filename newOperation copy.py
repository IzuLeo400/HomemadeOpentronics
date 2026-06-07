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
        "Base": reservoir_24["A3"], 
        "A_Mix": reservoir_24["A2"], "T_Mix": reservoir_24["B2"], "G_Mix": reservoir_24["C2"], "C_Mix": reservoir_24["D2"],
    }
    Dest = {
        "A": reservoir_24["A2"], "T": reservoir_24["B2"], "G": reservoir_24["C2"], "C": reservoir_24["D2"],
        "A_Mix": reservoir_24["A2"], "T_Mix": reservoir_24["B2"], "G_Mix": reservoir_24["C2"], "C_Mix": reservoir_24["D2"],
    }
    def transfer(Liquid, Volume, Destination=None, Name="Untitled") -> None:
        pipette_left.pick_up_tip(tip_rack.wells()[TipRackOrganization[Liquid]])
        pipette_left.aspirate(Volume, Source[Liquid])
        pipette_left.dispense(Volume, Dest[Liquid] if Destination==None else Destination)
        pipette_left.return_tip()

    def mix(Type) -> None:
        pipette_left.pick_up_tip(tip_rack.wells()[TipRackOrganization[Type]])
        pipette_left.mix(5, 50, Dest[Type])
        pipette_left.return_tip()
    
    def process(Letter) -> None:
        # PROTOCOL STEPS
        transfer("Wash", 1000, column_holder["A1"], "Wash1 -> ColumnHolder")
        transfer("Wash", 1000, column_holder["A1"], "Wash2 -> ColumnHolder")
        transfer(Letter, 120, Name="Monomer {Letter} -> Mix {Letter}")
        transfer("Base", 30, Dest[Letter], Name="Base -> Mix {Letter}")
        mix("{Letter}_Mix")
        transfer("{Letter}_Mix", 120, column_holder["A1"], "Mix {Letter} -> ColumnHolder")
        protocol.delay(seconds=30, msg="column mix pause")
        transfer("WashOH", 800, column_holder["A1"], "WashOH -> ColumnHolder")
        transfer("Deprotect", 800, column_holder["A1"], "Deprotect -> ColumnHolder")
        protocol.delay(seconds=10, msg="wash pause")

    String = "CCTCCTTACCTCAGTTACAATTTATA"
    for letter in String:
        process(letter)

CUSTOM_LABWARE = json.loads("""{"custom_beta/danny_1_reservoir_350000ul/1":{"ordering":[["A1"]],"brand":{"brand":"Danny","brandId":["Danny'sStuff"]},"metadata":{"displayName":"Danny 1 Reservoir 350000 µL","displayCategory":"reservoir","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.5,"yDimension":85.4,"zDimension":110},"wells":{"A1":{"depth":106,"totalLiquidVolume":350000,"shape":"circular","diameter":80,"x":63.75,"y":42.7,"z":4}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1"]}],"parameters":{"format":"irregular","quirks":["centerMultichannelOnWells","touchTipDisabled"],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"danny_1_reservoir_350000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}},"custom_beta/dan_24_reservoir_4000ul/1":{"ordering":[["A1","B1","C1","D1"],["A2","B2","C2","D2"],["A3","B3","C3","D3"],["A4","B4","C4","D4"],["A5","B5","C5","D5"],["A6","B6","C6","D6"]],"brand":{"brand":"Dan","brandId":["Dan2"]},"metadata":{"displayName":"Dan 24 Reservoir 4000 µL","displayCategory":"reservoir","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.47,"zDimension":46},"wells":{"A1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":72.17,"z":2},"B1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":52.67,"z":2},"C1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":33.17,"z":2},"D1":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":14.9,"y":13.67,"z":2},"A2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":72.17,"z":2},"B2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":52.67,"z":2},"C2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":33.17,"z":2},"D2":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":34.4,"y":13.67,"z":2},"A3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":72.17,"z":2},"B3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":52.67,"z":2},"C3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":33.17,"z":2},"D3":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":53.9,"y":13.67,"z":2},"A4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":72.17,"z":2},"B4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":52.67,"z":2},"C4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":33.17,"z":2},"D4":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":73.4,"y":13.67,"z":2},"A5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":72.17,"z":2},"B5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":52.67,"z":2},"C5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":33.17,"z":2},"D5":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":92.9,"y":13.67,"z":2},"A6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":72.17,"z":2},"B6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":52.67,"z":2},"C6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":33.17,"z":2},"D6":{"depth":44,"totalLiquidVolume":4000,"shape":"circular","diameter":13,"x":112.4,"y":13.67,"z":2}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1","B1","C1","D1","A2","B2","C2","D2","A3","B3","C3","D3","A4","B4","C4","D4","A5","B5","C5","D5","A6","B6","C6","D6"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"dan_24_reservoir_4000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}},"custom_beta/columnholder_5_wellplate_100000ul/1":{"ordering":[["A1"],["A2"],["A3"],["A4"],["A5"]],"brand":{"brand":"ColumnHolder","brandId":["DanYijia"]},"metadata":{"displayName":"ColumnHolder 5 Well Plate 100000 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":87},"wells":{"A1":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":19.8,"y":42.74,"z":42},"A2":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":41.8,"y":42.74,"z":42},"A3":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":63.8,"y":42.74,"z":42},"A4":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":85.8,"y":42.74,"z":42},"A5":{"depth":45,"totalLiquidVolume":100000,"shape":"circular","diameter":9,"x":107.8,"y":42.74,"z":42}},"groups":[{"metadata":{"wellBottomShape":"flat"},"wells":["A1","A2","A3","A4","A5"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"columnholder_5_wellplate_100000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")