TRACK_NAMES = [
    "byof",
    "Watches In My Bedsheets (ft. KAS)",
    "Bored (ft. KAS)",
    "Ollasong (ft. Savvy-Funk)",
    "Goner",
    "Saint Iker",
    "Nightlove (ft. Kas)",
    "Peach and Smoke",
    "Dead Fires",
    "First Town Down",
    "Happy Talk",
    "98 Degrees",
]

AUDIO_EXTENSION = "mp3"
ORIGINAL_AUDIO_BASE_PATH = "../assets/audio/original"

ORIGINAL_AUDIO_FILEPATHS = [
    "{0}/{1:02d} {2}.{3}".format(
        ORIGINAL_AUDIO_BASE_PATH,
        (index + 1),
        track,
        AUDIO_EXTENSION,
    ) for (index, track) in enumerate(TRACK_NAMES)
]

BASE_IMAGE_SUBMISSION_PATH = "assets/images/submissions"

IMAGE_SUBMISSION_PATHS = {
    "ACCEPTED": BASE_IMAGE_SUBMISSION_PATH + "/accepted",
    "REJECTED": BASE_IMAGE_SUBMISSION_PATH + "/rejected",
    "PENDING": BASE_IMAGE_SUBMISSION_PATH + "/pending",
}
