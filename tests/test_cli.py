import subprocess 
import sys
import os

def test_sample_option():
    result = subprocess.run(
        [sys.executable, os.path.join('src','ngram.py'),os.path.join('tests','test.txt'),'--s'], 
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "this is just a test"

def test_sample_option_displays_50_words():
    result = subprocess.run(
        [sys.executable,os.path.join('src','ngram.py'),os.path.join('tests','test.txt'),'--s'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert len(result.stdout.strip().join(" ")) < 50
