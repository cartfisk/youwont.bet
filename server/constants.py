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
AUDIO_BASE_PATH = "assets/audio/original"
AUDIO_FILEPATHS = [
    "{0}/{1:02d} {2}.{3}".format(
        AUDIO_BASE_PATH,
        (index + 1),
        track,
        AUDIO_EXTENSION,
    ) for (index, track) in enumerate(TRACK_NAMES)
]
AUDIO_ARCHIVE_PATH = "assets/audio/archive/pace-yourself.zip"

BASE_IMAGE_SUBMISSION_PATH = "assets/images/submissions"
IMAGE_SUBMISSION_PATHS = {
    "ACCEPTED": BASE_IMAGE_SUBMISSION_PATH + "/accepted",
    "REJECTED": BASE_IMAGE_SUBMISSION_PATH + "/rejected",
    "PENDING": BASE_IMAGE_SUBMISSION_PATH + "/pending",
}
MASTER_IMAGE_PATH = "assets/images/composite/master.png"
