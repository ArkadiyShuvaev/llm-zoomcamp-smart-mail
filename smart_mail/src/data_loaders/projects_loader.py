from typing import List
import uuid
from common.emails import get_email_with_investments_in_project1, get_email_with_investments_in_project2

from dtos.project import Project


class ProjectsLoader:
    """Agent to return a list of the projects"""

    @staticmethod
    def get_projects_by_email(email: str) -> List[Project]:
        if email == get_email_with_investments_in_project1():
            return [
                Project.create(uuid.UUID("00000000-0000-0000-0000-000000000001"), "Fake project 1"),
                Project.create(uuid.UUID("0113C948-C9CE-4A3D-AF99-D66BDEDE7D33"), "The Five"),
                Project.create(uuid.UUID("D1F21F84-9EEC-4D0B-A63A-BF656A28A256"), "DFI Zukunftspark Oberfranken V"),
                Project.create(uuid.UUID("716867B4-C28C-425E-94BE-59886D853D49"), "Berliner Flair in Friedrichshain II")
            ]

        if email == get_email_with_investments_in_project2():
            return [
                Project.create(uuid.UUID("00000000-0000-0000-0000-000000000002"), "Fake project 2"),
                Project.create(uuid.UUID("2e239357-4967-40e6-807e-b9eb87fab5ad"), "Pracht-Altbau Sendlinger Tor")
            ]

        return []

    @staticmethod
    def get_projects() -> List[Project]:
        return [
            Project.create(uuid.UUID("54EE27F7-BFB3-49BD-9438-2BE412C8D8A0"), "DFI Zukunftspark Oberfranken VI"),
            Project.create(uuid.UUID("716867B4-C28C-425E-94BE-59886D853D49"), "Berliner Flair in Friedrichshain II"),
            Project.create(uuid.UUID("E2FEFD3E-6841-434F-AF12-6E700D7C60D3"), "DFI Zukunftspark Nordbayern IV"),
            Project.create(uuid.UUID("D1F21F84-9EEC-4D0B-A63A-BF656A28A256"), "DFI Zukunftspark Oberfranken V"),
            Project.create(uuid.UUID("811DC8A3-C453-48A0-82DD-58DF3AD52A6D"), "Am Akkonplatz"),
            Project.create(uuid.UUID("83FF1D1C-6A7F-45BB-ADFF-0E42C26463A4"), "Berliner Flair in Friedrichshain"),
            Project.create(uuid.UUID("E6EA9000-8561-4F86-8795-A60032F239F4"), "DFI Zukunftspark Oberfranken IV"),
            Project.create(uuid.UUID("4973E74A-E88E-4E1B-B534-36615368D4A6"), "Tonhallen-Passage II"),
            Project.create(uuid.UUID("35F259F1-4160-4768-9C7A-9ECBDA485BA0"), "DFI Zukunftspark Nordbayern III"),
            Project.create(uuid.UUID("41E842BB-6963-4CE9-BC24-1C0A58648D7A"), "DFI Zukunftspark Oberfranken III"),
            Project.create(uuid.UUID("BAFBFF1D-8953-48DD-922F-95489B0334FA"), "DFI Zukunftspark Dreiländereck II"),
            Project.create(uuid.UUID("A0D1803B-9018-4774-82A4-AAB4668E19C6"), "Friedrichstraße 191 III"),
            Project.create(uuid.UUID("2263D038-4EC4-4147-B116-78D728F19CE2"), "Office am Europaring IV"),
            Project.create(uuid.UUID("8F43C311-FFC4-48FF-9FEC-96F2DA8006FD"), "DFI Zukunftspark Mittelfranken"),
            Project.create(uuid.UUID("9C0D39D1-E98B-4C90-BE38-A3C6CC02E79A"), "Wohnquartier Pasing II"),
            Project.create(uuid.UUID("E391251B-C6C5-46D9-AA54-6B0385CC530C"), "DFI Zukunftspark Dreiländereck"),
            Project.create(uuid.UUID("4E10CBD1-7D59-42E7-A0E9-27A6446CFC2B"), "smart-UP Self-Storage-Park III"),
            Project.create(uuid.UUID("4D8F9F51-556B-4AD5-8223-7F7B96F16EBE"), "Stadthaus Mozart IV"),
            Project.create(uuid.UUID("180770C4-5FE2-481B-B2CF-6BEF10A9B400"), "Stadthaus Mozart III"),
            Project.create(uuid.UUID("04DF54CA-2B08-4545-ADD1-EA4D6301E993"), "Büro-Hochhaus am Scheidemannplatz II"),
            Project.create(uuid.UUID("F076C5A5-740E-476B-AA35-9B25389E0A82"), "smartUP Self-Storage-Park II"),
            Project.create(uuid.UUID("F69E47F1-B3A3-41E1-BDCB-72FE1C097790"), "Jugendstil-Altbau am Rothenbaum II"),
            Project.create(uuid.UUID("964AEB7E-D162-4AD6-BBCB-8B238C6A047A"), "Stadtleben Altlindenau"),
            Project.create(uuid.UUID("755DB000-4F7C-4AD6-A4A0-C7EA67B26C2E"), "An der Kleinen Weser"),
            Project.create(uuid.UUID("94FB4C8A-1FFA-42E1-9F2C-A185C9DB0081"), "Modernes Wohnen am Nymphenburger Kanal II"),
            Project.create(uuid.UUID("FE352A6E-377A-4EF6-B41D-0D9B6BDD2F5B"), "Atelier-Wohnungen an der Burg II"),
            Project.create(uuid.UUID("771AAE7A-362C-4F0F-B969-32F29F19AF08"), "Eco Living Lichtenrade"),
            Project.create(uuid.UUID("0113C948-C9CE-4A3D-AF99-D66BDEDE7D33"), "The Five"),
            Project.create(uuid.UUID("FE5B1D79-7AF1-4434-BEE0-9234DD98E384"), "Elegantes Wohnen nahe der Isar"),
            Project.create(uuid.UUID("710D7579-2500-480F-8169-E2350C2A6ABF"), "Solarpark Eyendorf"),
            Project.create(uuid.UUID("CEA056C8-E657-4051-A633-89D310ACECF7"), "DFI Zukunftspark Oberrhein II"),
            Project.create(uuid.UUID("689F8D79-AF06-4C23-8D14-7FB937E5E804"), "DFI Zukunftspark Nordbayern II"),
            # Project.create(uuid.UUID("CC215696-CDDF-43B2-BB79-BD204EFD64F3"), "Spendenprojekt - Green Forest Fund"),
            Project.create(uuid.UUID("5F74EEEB-0F8A-4A85-84B7-590EA468A2E6"), "Bürokomplex Alemannenhof III"),
            Project.create(uuid.UUID("2B23BAF6-503B-4A55-A4C2-52F075B681A9"), "DFI Zukunftspark Oberfranken II"),
            Project.create(uuid.UUID("280FBEAB-D3BC-47CD-AD6F-66ED4A55DC76"), "Office am Europaring III"),
            Project.create(uuid.UUID("C0EFFCBA-AB7D-4DB2-BBBD-DA72EF272C7E"), "DFI Zukunftspark Oberfranken"),
            Project.create(uuid.UUID("4148DC9F-28CD-44E5-AB22-6B3F9B0DEBB9"), "OVUM Neue Mitte Braunsfeld II"),
            Project.create(uuid.UUID("5B83ABAD-A280-492B-A74D-11EC2883A370"), "DFI Zukunftspark Nordbayern"),
            Project.create(uuid.UUID("118BBDEC-3A71-4E5F-B725-BDC85E4A31EB"), "Stadthaus 'Mozart'"),
            Project.create(uuid.UUID("AFDD98B3-B93C-4803-8D60-FF1733217768"), "Stadthaus 'Mozart' II"),
            Project.create(uuid.UUID("c827f162-6205-4688-84eb-6e1e2934595e"), "Pracht-Altbau Sendlinger Tor II"),
            Project.create(uuid.UUID("2e239357-4967-40e6-807e-b9eb87fab5ad"), "Pracht-Altbau Sendlinger Tor"),
        ]
