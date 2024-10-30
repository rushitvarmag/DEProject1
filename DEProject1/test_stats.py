from redactor import Redactor

def test_write_stats():
    redactor = Redactor()
    redactor.stats = {
        "names": 3,
        "dates": 2,
        "phones": 1,
        "addresses": 2,
        "concepts": 1
    }
    # Write stats to a mock file and check the output
    with open("test_stats_output.txt", 'w') as f:
        redactor.write_stats("test_stats_output.txt")

    with open("test_stats_output.txt", 'r') as f:
        stats_content = f.read()
        assert "names: 3" in stats_content
        assert "dates: 2" in stats_content
        assert "phones: 1" in stats_content
        assert "addresses: 2" in stats_content
        assert "concepts: 1" in stats_content
