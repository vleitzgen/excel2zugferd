"""
Module for handle_ini_file_test
"""

import os
import unittest
from pathlib import Path

import src.handle_ini_file as handle_ini_file


class TestIniFile(unittest.TestCase):
    """Testclass for IniFile"""

    def setUp(self) -> None:
        self.fn = "Test.ini"
        self.fn_import = "TestImport.ini"
        self.profile_file = "firma_profile.json"
        self.dir = "."
        self.file = os.path.join(self.dir, self.fn)
        self.file_import = os.path.join(self.dir, self.fn_import)
        self.profile_path = os.path.join(self.dir, self.profile_file)
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.file_import)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.profile_path)
        except FileNotFoundError:
            pass
        self.ini_file_class = handle_ini_file.IniFile(path_to_inifile=self.file)
        return super().setUp()

    def tearDown(self) -> None:
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.file_import)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.profile_path)
        except FileNotFoundError:
            pass
        return super().tearDown()

    def test_exists_false(self):
        """
        Teste, dass kein ini File existiert
        """
        file = self.ini_file_class.exists_ini_file()
        self.assertIsNone(file, "Should be None, because ini file doesn't exist")

    def test_exists_true(self):
        """
        Teste, ob ein ini File existiert
        """
        expected = {
            "Test1": "Irgendwas",
            "Test3": "Was anderes",
            "Test2": "Ganz was anderes",
        }
        self.ini_file_class.create_ini_file(expected)
        file = self.ini_file_class.exists_ini_file()
        self.assertIsNotNone(
            file, "Should not be None (File-Handle), because ini file exist"
        )
        content = self.ini_file_class.read_ini_file()
        self.assertDictEqual(
            content,
            expected,
            f"Content of Ini-File should be equal to {expected}",
            # type: ignore
        )

    def test_merge_content_of_ini_file(self):
        """
        Test the merge of content of ini_file with other content
        """
        MSG = "dicts should be equal"
        self.ini_file_class.content = {
            "Org1": "Test1",
            "Org2": "Test2",
            "Org3": "Test3",
        }
        modification = {"Org2": "Test4", "Mod1": "Test5"}
        expected = {"Org1": "Test1", "Org2": "Test4", "Org3": "Test3", "Mod1": "Test5"}
        self.ini_file_class.merge_content_of_ini_file(modification)
        self.assertDictEqual(self.ini_file_class.content, expected, MSG)

    def test_raise_error_on_false_ini_file(self):
        """
        Test the raise error if ini directory is not creatable
        """
        with self.assertRaises(ValueError):
            handle_ini_file.IniFile(dir=Path("I:/Laber"))

    def test_company_profile_helpers_return_active_company(self):
        """
        Mehrere Firmen sollen in einer Ini-Datei gespeichert werden können.
        """
        self.ini_file_class.content = {
            "Verzeichnis": "C:/tmp",
            "AktiveFirma": "Firma B",
            "Firmen": {
                "Firma A": {
                    "Betriebsbezeichnung": "Firma A GmbH",
                    "IBAN": "A-IBAN",
                },
                "Firma B": {
                    "Betriebsbezeichnung": "Firma B GmbH",
                    "IBAN": "B-IBAN",
                },
            },
        }

        self.assertEqual(
            self.ini_file_class.get_company_names(), ["Firma A", "Firma B"]
        )
        self.assertEqual(self.ini_file_class.get_active_company_name(), "Firma B")

        current = self.ini_file_class.get_active_company_content()
        self.assertEqual(current["Betriebsbezeichnung"], "Firma B GmbH")
        self.assertEqual(current["IBAN"], "B-IBAN")
        self.assertEqual(current["Verzeichnis"], "C:/tmp")

    def test_company_profile_helpers_work_without_profiles(self):
        """
        Die bisherige Ein-Firma-Struktur soll weiter funktionieren.
        """
        self.ini_file_class.content = {
            "Betriebsbezeichnung": "Legacy GmbH",
            "IBAN": "LEGACY-IBAN",
        }

        self.assertEqual(self.ini_file_class.get_company_names(), [])
        self.assertIsNone(self.ini_file_class.get_active_company_name())

        current = self.ini_file_class.get_active_company_content()
        self.assertEqual(current["Betriebsbezeichnung"], "Legacy GmbH")
        self.assertEqual(current["IBAN"], "LEGACY-IBAN")

    def test_save_and_switch_company_profile(self):
        """
        Eine neue Firma soll gespeichert und aktiv geschaltet werden können.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}

        self.ini_file_class.save_company(
            "Firma A",
            {
                "Betriebsbezeichnung": "Firma A GmbH",
                "IBAN": "A-IBAN",
            },
        )
        self.ini_file_class.save_company(
            "Firma B",
            {
                "Betriebsbezeichnung": "Firma B GmbH",
                "IBAN": "B-IBAN",
            },
        )

        self.assertEqual(self.ini_file_class.get_company_names(), ["Firma A", "Firma B"])
        self.assertEqual(self.ini_file_class.get_active_company_name(), "Firma A")

        self.ini_file_class.set_active_company("Firma B")
        self.assertEqual(self.ini_file_class.get_active_company_name(), "Firma B")
        self.assertEqual(
            self.ini_file_class.get_active_company_content()["Betriebsbezeichnung"],
            "Firma B GmbH",
        )

    def test_delete_company_profile_and_keep_remaining_active(self):
        """
        Löschen einer Firma soll auf verbleibende Firma umschalten.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}
        self.ini_file_class.save_company(
            "Firma A",
            {"Betriebsbezeichnung": "Firma A GmbH", "IBAN": "A-IBAN"},
        )
        self.ini_file_class.save_company(
            "Firma B",
            {"Betriebsbezeichnung": "Firma B GmbH", "IBAN": "B-IBAN"},
        )
        self.ini_file_class.set_active_company("Firma B")

        self.ini_file_class.delete_company("Firma B")

        self.assertEqual(self.ini_file_class.get_company_names(), ["Firma A"])
        self.assertEqual(self.ini_file_class.get_active_company_name(), "Firma A")
        self.assertEqual(
            self.ini_file_class.get_active_company_content()["Betriebsbezeichnung"],
            "Firma A GmbH",
        )

    def test_empty_company_name_raises_value_error(self):
        """
        Leere Firmennamen dürfen nicht gespeichert oder aktiviert werden.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}

        with self.assertRaises(ValueError):
            self.ini_file_class.save_company(
                "  ",
                {"Betriebsbezeichnung": "Ungültig"},
            )

        with self.assertRaises(ValueError):
            self.ini_file_class.set_active_company("   ")

    def test_rename_company_profile(self):
        """
        Umbenennen einer Firma soll den aktiven Namen aktualisieren.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}
        self.ini_file_class.save_company(
            "Firma A",
            {"Betriebsbezeichnung": "Firma A GmbH", "IBAN": "A-IBAN"},
        )
        self.ini_file_class.set_active_company("Firma A")

        self.ini_file_class.rename_company("Firma A", "Firma Neu")

        self.assertEqual(self.ini_file_class.get_company_names(), ["Firma Neu"])
        self.assertEqual(self.ini_file_class.get_active_company_name(), "Firma Neu")
        self.assertEqual(
            self.ini_file_class.get_active_company_content()["Betriebsbezeichnung"],
            "Firma Neu",
        )

    def test_export_and_import_company_profile(self):
        """
        Exportiertes Firmenprofil soll in eine andere Ini importierbar sein.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}
        self.ini_file_class.save_company(
            "Export GmbH",
            {"Betriebsbezeichnung": "Export GmbH", "IBAN": "EX-IBAN"},
        )

        self.ini_file_class.export_company_profile("Export GmbH", self.profile_path)

        target_ini = handle_ini_file.IniFile(path_to_inifile=self.file_import)
        imported_name = target_ini.import_company_profile(self.profile_path)

        self.assertEqual(imported_name, "Export GmbH")
        self.assertEqual(target_ini.get_active_company_name(), "Export GmbH")
        self.assertEqual(
            target_ini.get_active_company_content()["IBAN"],
            "EX-IBAN",
        )

    def test_import_company_profile_creates_unique_name_on_conflict(self):
        """
        Bei Namenskonflikten soll beim Import ein neuer Name erzeugt werden.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}
        self.ini_file_class.save_company(
            "Export GmbH",
            {"Betriebsbezeichnung": "Export GmbH", "IBAN": "EX-IBAN-1"},
        )
        self.ini_file_class.export_company_profile("Export GmbH", self.profile_path)

        target_ini = handle_ini_file.IniFile(path_to_inifile=self.file_import)
        target_ini.save_company(
            "Export GmbH",
            {"Betriebsbezeichnung": "Export GmbH", "IBAN": "EX-IBAN-0"},
        )

        imported_name = target_ini.import_company_profile(self.profile_path)

        self.assertEqual(imported_name, "Export GmbH (2)")
        self.assertEqual(target_ini.get_active_company_name(), "Export GmbH (2)")
        self.assertEqual(
            target_ini.get_active_company_content()["Betriebsbezeichnung"],
            "Export GmbH (2)",
        )

    def test_save_current_company_content_ignores_profile_metadata(self):
        """
        Metadaten wie 'Firmen'/'AktiveFirma' dürfen nicht ins Firmenprofil kopiert werden.
        """
        self.ini_file_class.content = {"Verzeichnis": "C:/tmp"}
        self.ini_file_class.save_company(
            "Firma A",
            {"Betriebsbezeichnung": "Firma A", "IBAN": "A-IBAN"},
        )

        full_content = self.ini_file_class.content
        self.ini_file_class.save_current_company_content(full_content)

        profile = self.ini_file_class.content["Firmen"]["Firma A"]
        self.assertNotIn("Firmen", profile)
        self.assertNotIn("AktiveFirma", profile)


# if __name__ == '__main__':
#     unittest.main()
