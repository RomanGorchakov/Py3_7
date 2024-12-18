import argparse
import sqlite3
import typing as t
from pathlib import Path
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict, field


@dataclass
class Plane:
    race: str
    number: int
    type: int

@dataclass
class PlaneManager:
    planes: t.List[Plane] = field(default_factory=list)

    def add_plane(self, plane: Plane) -> None:
        self.planes.append(plane)

    def to_xml(self, filepath: Path) -> None:
        root = ET.Element("planes")
        for plane in self.planes:
            plane_elem = ET.SubElement(root, "plane")
            for key, value in asdict(plane).items():
                child = ET.SubElement(plane_elem, key)
                child.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def from_xml(self, filepath: Path) -> None:
        tree = ET.parse(filepath)
        root = tree.getroot()
        self.planes = []
        for plane_elem in root.findall("plane"):
            data = {child.tag: child.text for child in plane_elem}
            self.planes.append(Plane(
                race=data["race"],
                number=int(data["number"]),
                type=int(data["type"])
            ))

def create_db(database_path: Path) -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name TEXT NOT NULL,
            number_name INTEGER NOT NULL,
            type_name INTEGER NOT NULL,
            FOREIGN KEY(race_name) REFERENCES cities(race_name)
        )
        """
    )

    conn.close()

def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "workers.db"),
        help="The database file name"
    )

    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.2.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new race"
    )
    add.add_argument(
        "-r",
        "--race",
        action="store",
        required=True,
        help="The city where the plane will go"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        required=True,
        help="The number of the race"
    )
    add.add_argument(
        "-t",
        "--type",
        action="store",
        type=int,
        required=True,
        help="The type of the plane"
    )

    save = subparsers.add_parser(
        "save",
        parents=[file_parser],
        help="Save data to XML"
    )
    save.add_argument(
        "--file",
        action="store",
        required=True,
        help="The XML file to save data"
    )

    load = subparsers.add_parser(
        "load",
        parents=[file_parser],
        help="Load data from XML"
    )
    load.add_argument(
        "--file",
        action="store",
        required=True,
        help="The XML file to load data"
    )

    args = parser.parse_args(command_line)
    db_path = Path(args.db)
    create_db(db_path)

    manager = PlaneManager()

    if args.command == "add":
        plane = Plane(race=args.race, number=args.number, type=args.type)
        manager.add_plane(plane)

    elif args.command == "save":
        xml_path = Path(args.file)
        manager.to_xml(xml_path)

    elif args.command == "load":
        xml_path = Path(args.file)
        manager.from_xml(xml_path)
        for plane in manager.planes:
            print(f"Loaded plane: {plane}")

if __name__ == "__main__":
    main()
