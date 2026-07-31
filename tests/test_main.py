from main import main


def test_main_prints_expected_message(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from personal-research-agent\n"
    assert captured.err == ""
