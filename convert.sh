#!/bin/bash

# Sprawdź, czy imagemagick jest zainstalowany
if ! command -v convert &> /dev/null; then
    echo "imagemagick nie jest zainstalowany. Zainstaluj go, aby kontynuować."
    echo "Możesz go zainstalować za pomocą:"
    echo "sudo apt install imagemagick  # Dla Ubuntu/Debian"
    echo "sudo brew install imagemagick # Dla macOS"
    exit 1
fi

# Wyszukaj wszystkie pliki .avif w bieżącym folderze i podfolderach
find . -type f -iname "*.avif" | while read -r file; do
    # Określ nazwę pliku wyjściowego (zamień .avif na .jpeg)
    output_file="${file%.avif}.jpeg"

    # Konwertuj plik .avif na .jpeg
    echo "Konwertuję: $file -> $output_file"
    convert "$file" "$output_file"

    # Sprawdź, czy konwersja się powiodła
    if [ $? -eq 0 ]; then
        echo "Konwersja zakończona sukcesem."
    else
        echo "Błąd podczas konwersji: $file"
    fi
done

echo "Wszystkie pliki .avif zostały przetworzone."
