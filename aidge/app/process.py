import os
import shutil


def process_file(input_path: str, config: dict) -> str:
    """Traite le fichier uploadé et retourne le path du dossier de sortie."""
    output_dir = os.path.join(os.path.dirname(input_path), "output")
    os.makedirs(output_dir)

    # Exemple : copie du fichier traité
    filename = os.path.basename(input_path)
    shutil.copy(input_path, os.path.join(output_dir, filename))

    return output_dir
