#!/usr/bin/env python3

import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser()
    parser.add_argument("--language", choices=["c", "cpp"], default="c", help="Language of the contract")
    parser.add_argument("--llvm", type=int, required=True, help="LLVM version to be used")
    parser.add_argument("--path", required=True, help="Path to the contract folder")

    args = parser.parse_args()

    language = args.language
    llvm_version = args.llvm
    input_folder = Path(args.path).expanduser().resolve()
    output_folder = input_folder / "output"

    if language == "c":
        do_build_c(input_folder, output_folder, llvm_version)
    elif language == "cpp":
        do_build_cpp(input_folder, output_folder, llvm_version)
    else:
        print(f"Unknown language: {language}.")
        exit(1)

    print("Done.")


def do_build_c(input_folder: Path, output_folder: Path, llvm_version: str):
    source_files = sorted(input_folder.rglob("*.c"))

    if not source_files:
        print("No source files found.")
        exit(1)

    first_unit_file = source_files[0]
    contract_name = first_unit_file.stem
    export_file = first_unit_file.with_suffix(".export")

    if not export_file.exists():
        print(f"Export file {export_file} does not exist.")
        exit(1)

    clang = f"clang-{llvm_version}"
    llvm_link = f"llvm-link-{llvm_version}"
    llc = f"llc-{llvm_version}"
    wasm_ld = f"wasm-ld-{llvm_version}"

    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()

    main_bc_path = output_folder / "__main.bc"
    main_obj_path = output_folder / "__main.o"

    for source_file in source_files:
        subprocess.check_call([
            clang,
            "-cc1",
            "-emit-llvm",
            "-triple=wasm32-unknown-unknown-wasm",
            "-o",
            str(output_folder / f"{source_file.stem}.ll"),
            "-O0",
            source_file
        ])

    ll_files = sorted(list(output_folder.rglob("*.ll")))

    subprocess.check_call([
        llvm_link,
        "-o",
        str(main_bc_path),
        *ll_files
    ])

    subprocess.check_call([
        llc,
        "-O0",
        "-filetype=obj",
        str(main_bc_path),
        "-o",
        str(main_obj_path),
    ])

    exported_endpoints = [line.strip() for line in export_file.read_text().splitlines() if line.strip()]
    export_arguments = [f"--export={endpoint}" for endpoint in exported_endpoints]

    subprocess.check_call([
        wasm_ld,
        "--no-entry",
        str(main_obj_path),
        "-o",
        str(output_folder / f"{contract_name}.wasm"),
        "--strip-all",
        "--allow-undefined",
        *export_arguments
    ])

    # Cleanup
    main_bc_path.unlink()
    main_obj_path.unlink()

    for ll_file in ll_files:
        ll_file.unlink()


def do_build_cpp(input_folder: Path, output_folder: Path, llvm_version: str):
    raise NotImplementedError()


if __name__ == "__main__":
    main()
