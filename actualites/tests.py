from django.test import SimpleTestCase


class LegacyRedirectTests(SimpleTestCase):
    def test_legacy_presse_article_redirects_to_actualite(self):
        response = self.client.get("/presse/rapport-sondage-2025/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/actualites/rapport-sondage-2025/")

    def test_legacy_presse_article_redirect_accepts_missing_trailing_slash(self):
        response = self.client.get("/presse/rapport-sondage-2025")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/actualites/rapport-sondage-2025/")

    def test_legacy_mission_page_redirects_to_a_propos(self):
        response = self.client.get("/mission/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/a-propos/")

    def test_another_legacy_presse_article_redirects_to_actualite(self):
        response = self.client.get("/presse/petition-glyphosate/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/actualites/petition-glyphosate/")

    def test_legacy_presse_redirect_preserves_query_string(self):
        response = self.client.get("/presse/rapport-sondage-2025/?utm_source=google")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "/actualites/rapport-sondage-2025/?utm_source=google",
        )
