import random


def generate_log_files():
    num_files = random.randint(1, 5)

    for i in range(1, num_files + 1):
        formatted_number = "{:05d}".format(i)
        mission_chosen = random.choice(["ORBONE", "CLNM", "TMRS", "GALXTWO", "UNKN"])
        file_name = (
            f"APL{mission_chosen}-{formatted_number}.log"  # Cambié la extensión a .log
        )
        content = generate_random_log_content()

        with open(file_name, "w") as file:
            file.write(content)

        print(f"Archivo {file_name} creado.")


def generate_random_log_content():
    log_levels = ["date", "mission", "device_type", "device_status", "hash"]
    log_messages = [
        "Something happened.",
        "An error occurred.",
        "System is running smoothly.",
    ]

    content = ""
    for _ in range(random.randint(1, 10)):
        log_entry = f"{random.choice(log_levels)}: {random.choice(log_messages)}\n"
        content += log_entry

    return content


# Llama a la función para generar los archivos de logs
# generate_log_files()
