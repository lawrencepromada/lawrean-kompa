import json
import time
import urllib.request
import uuid


URL = "http://127.0.0.1:8000/compare"

FILES = [
    ("original", "../sample-data/original.pdf"),
    ("revised", "../sample-data/revised.pdf"),
]


def build_multipart():
    boundary = uuid.uuid4().hex
    body = bytearray()

    for field_name, path in FILES:
        filename = path.replace("\\", "/").split("/")[-1]

        with open(path, "rb") as file:
            data = file.read()

        body.extend(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{filename}"\r\n'
                "Content-Type: application/pdf\r\n"
                "\r\n"
            ).encode()
        )

        body.extend(data)
        body.extend(b"\r\n")

    body.extend(
        f"--{boundary}--\r\n".encode()
    )

    return boundary, bytes(body)


times = []

print("Running 3 timing tests...\n")

for run in range(1, 4):
    boundary, body = build_multipart()

    request = urllib.request.Request(
        URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": (
                f"multipart/form-data; boundary={boundary}"
            ),
        },
    )

    start = time.perf_counter()

    try:
        with urllib.request.urlopen(request) as response:
            result = json.load(response)

    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}")

        error_body = error.read().decode(
            "utf-8",
            errors="replace",
        )

        print(error_body)
        raise

    elapsed = time.perf_counter() - start
    api_time = result["processing_time_seconds"]

    times.append(elapsed)

    print(
        f"Run {run}: "
        f"{elapsed:.3f}s client total | "
        f"{api_time:.3f}s API processing"
    )


average = sum(times) / len(times)

print("\n=== Timing Summary ===")
print(f"Average client time: {average:.3f}s")
print(f"Fastest: {min(times):.3f}s")
print(f"Slowest: {max(times):.3f}s")