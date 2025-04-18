class TextCleaner:
    """Utility class for cleaning retrieved text."""
    
    @staticmethod
    def clean_text(text):
        """Remove common boilerplate and format text for readability."""
        phrases_to_remove = [
            'http://www.davince.com', 'http://www.davince.com/bible',
            'Downloaded from www.holybooks.com - https://www.holybooks.com/download-bible/',
            "Downloaded from www.holybooks.com", "- https://www.holybooks.com/download-bible/",
            "www.krishna.com", "Copyright © 1998 The Bhaktivedanta Book Trust Int'l. All Rights Reserved.",
            "\n", "\t"
        ]
        for phrase in phrases_to_remove:
            text = text.replace(phrase, "")
            text.encode("utf-8", "ignore").decode("utf-8").replace("\ufffd", "")

        return text.strip()