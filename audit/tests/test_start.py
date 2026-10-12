import importlib.util, itertools, os, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
spec = importlib.util.spec_from_file_location("kit_start", os.path.join(ROOT, "scripts", "kit_start.py"))
ks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ks)


def ans(**kw):
    d = dict(stage="production", hosting="managed-cloud", data="personal", framework="none", people="1-3")
    d.update(kw)
    return d


def flat(p):
    return p["now"] + p["next"] + p["later"]


class StartTests(unittest.TestCase):
    def test_every_combination_produces_a_plan_with_known_links(self):
        opts = [[o[0] for o in q[2]] for q in ks.QUESTIONS]
        n = 0
        for combo in itertools.product(*opts):
            a = dict(zip([q[0] for q in ks.QUESTIONS], combo))
            p = ks.plan(a)
            keys = flat(p)
            self.assertEqual(len(keys), len(set(keys)), a)          # no duplicates
            self.assertTrue(set(keys) <= set(ks.LINKS), a)           # every key has a link
            self.assertIn("01", p["now"])                            # access control always starts first
            n += 1
        self.assertEqual(n, 3 * 4 * 4 * 5 * 4)

    def test_every_link_points_at_a_real_file(self):
        for k, (text, path) in ks.LINKS.items():
            self.assertTrue(os.path.exists(os.path.join(ROOT, path)), f"{k}: {path}")

    def test_prelaunch_without_data_starts_with_secure_development(self):
        p = ks.plan(ans(stage="prelaunch", data="none"))
        self.assertIn("securedev", p["now"])
        self.assertNotIn("05", p["now"])
        self.assertIn("privacy", p["later"])

    def test_live_saas_with_personal_data_starts_with_backups_incident_privacy(self):
        p = ks.plan(ans())
        for k in ("05", "06", "09", "privacy"):
            self.assertIn(k, p["now"])

    def test_enterprise_adds_requirement_mapping_and_a_formal_decision(self):
        p = ks.plan(ans(stage="enterprise", framework="soc2"))
        self.assertIn("soc2", p["next"])
        self.assertIn("mapreq", p["next"])
        self.assertIn("formal", p["later"])

    def test_legacy_environment_restore_test_before_migration(self):
        p = ks.plan(ans(hosting="legacy"))
        self.assertIn("restore", p["now"])
        self.assertIn("migration", p["next"])

    def test_special_category_data_says_take_advice(self):
        self.assertIn("special", ks.plan(ans(data="special"))["now"])

    def test_larger_teams_get_joiner_leaver_and_policies(self):
        p = ks.plan(ans(people="11-50"))
        for k in ("joiners", "accessreview", "policies", "training"):
            self.assertIn(k, p["next"])
        self.assertNotIn("policies", flat(ks.plan(ans(people="1-3"))))

    def test_no_framework_means_do_not_chase_one(self):
        self.assertNotIn("soc2", flat(ks.plan(ans(framework="none"))))
        self.assertIn("Do not pursue a formal framework", ks.render(ans()))

    def test_command_line_with_all_answers_runs_without_a_terminal(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ks.main(["--stage", "production", "--hosting", "managed-cloud", "--data", "personal",
                          "--framework", "questionnaires", "--people", "4-10"])
        self.assertEqual(rc, 0)
        self.assertIn("## Do now (this week)", buf.getvalue())


    def test_personal_data_prompts_the_gdpr_scope_check_but_not_when_there_is_none(self):
        self.assertIn("gdprscope", ks.plan(ans(stage="production", data="personal"))["now"])
        self.assertIn("gdprscope", ks.plan(ans(stage="prelaunch", data="personal"))["next"])
        for d in ("none", "business"):
            self.assertNotIn("gdprscope", flat(ks.plan(ans(data=d))))

    def test_invalid_answers_are_rejected(self):
        for bad in (["--stage", "bogus"], ["--people", "7"], ["--framework", "gdpr"]):
            with self.assertRaises(SystemExit) as cm:
                ks.main(bad)
            self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
