import pytest
from brute import Brute
from unittest.mock import Mock




def describe_brute():
    def it_hashes_target_when_creating_constructor():
        brute = Brute("password123")
        expected_target = brute.hash("password123")
        print(brute.target)
        assert brute.target == expected_target
    
    def it_returns_true_when_brute_once_is_successful():
        brute = Brute("test")
        attempt = "test"
        assert brute.bruteOnce(attempt) is True
    
    def it_returns_false_when_brute_once_is_unsuccessful():
        brute = Brute("test")
        attempt = "wrong"
        assert brute.bruteOnce(attempt) is False

    def it_returns_false_when_capitalization_is_incorrect():
        brute = Brute("Test")
        attempt = "teSt"
        assert brute.bruteOnce(attempt) is False
    
    def it_will_guess_password_within_limit_using_set_limit():
        brute = Brute("Test")

        def mock_random_guess():
            return "Test"

        brute.randomGuess = Mock(side_effect=mock_random_guess)


        result = brute.bruteMany(limit=10)
        assert result != -1
        brute.randomGuess.assert_called()
    
    def it_will_guess_password_within_limit_using_default_limit():
        brute = Brute("Test")

        def mock_random_guess():
            return "Test"

        brute.randomGuess = Mock(side_effect=mock_random_guess)

        result = brute.bruteMany()
        assert result != -1
    
    def it_will_fail_to_guess_password_within_default_limit():
        brute = Brute("Test")

        def mock_random_guess():
            return "wrong password"
        brute.randomGuess = Mock(side_effect=mock_random_guess)
        result = brute.bruteMany()
        assert result == -1
        assert brute.randomGuess.call_count == 10000000
    
    def it_will_fail_to_guess_password_within_set_limit():
        brute = Brute("Test")
        
        def mock_random_guess():
            return "wrong password"
        brute.randomGuess = Mock(side_effect=mock_random_guess)
        result = brute.bruteMany(limit=50)
        assert result == -1
        assert brute.randomGuess.call_count == 50
    
    def it_will_fail_to_guess_password_with_zero_limit():
        brute = Brute("Test")
        result = brute.bruteMany(limit=0)
        assert result == -1
    
    def it_will_fail_to_guess_password_when_given_empty_string():
        brute = Brute("")
        result = brute.bruteMany()
        assert result == -1
    

    
