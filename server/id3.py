from mutagen.id3 import ID3, APIC

def update_id3_tags(track_paths, artwork_path, artwork_mimetype="image/png"):
    for track_path in tracks:

        audio = ID3(track_path)

        with open(artwork_path, "rb") as albumart:
            audio["APIC"] = APIC(
                              encoding=3,
                              mime=artwork_mimetype,
                              type=3, desc=u"Cover",
                              data=albumart.read()
                            )

        audio.save()
