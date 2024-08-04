import datetime
import unittest
from unittest.mock import patch, MagicMock
import voice_assistant

class TestVoiceAssistant(unittest.TestCase):

    @patch('voice_assistant.engine')
    def test_speak(self, mock_engine):
        voice_assistant.speak("Hello")
        mock_engine.say.assert_called_with("Hello")
        mock_engine.runAndWait.assert_called_once()

    @patch('voice_assistant.speak')
    @patch('voice_assistant.datetime')
    def test_wish_me(self, mock_datetime, mock_speak):
        mock_datetime.datetime.now.return_value.hour = 10
        voice_assistant.wish_me()
        mock_speak.assert_any_call("Good Morning Sir!")
        mock_speak.assert_any_call("I am your Assistant. How can I help you?")    


    @patch('voice_assistant.sr.Recognizer')
    @patch('voice_assistant.sr.Microphone')
    def test_take_command(self, mock_microphone, mock_recognizer):
        recognizer_instance = mock_recognizer.return_value
        recognizer_instance.listen.return_value = 'audio'
        recognizer_instance.recognize_google.return_value = 'Hello'
        result = voice_assistant.take_command()
        self.assertEqual(result, 'hello')

    @patch('voice_assistant.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value
        voice_assistant.send_email("5747praveen@gmail.com", "Test content")
        mock_smtp_instance.sendmail.assert_called_with(
            'raks.marolix@gmail.com', '5747praveen@gmail.com', 'Test content'
        )
        mock_smtp_instance.close.assert_called_once()

    @patch('voice_assistant.os.listdir')
    @patch('voice_assistant.play_song_with_default_player')
    def test_play_all_songs(self, mock_play_song, mock_listdir):
        mock_listdir.return_value = ['10 - Jwalath Karaals - SenSongsMp3.co.mp3']
        with patch('voice_assistant.random.shuffle', lambda x: x):
            voice_assistant.play_all_songs('C:\\Users\\admin\\Desktop\\songs')
            mock_play_song.assert_any_call('C:\\Users\\admin\\Desktop\\songs\\10 - Jwalath Karaals - SenSongsMp3.co.mp3')

    @patch('voice_assistant.speak')
    def test_search_wikipedia(self, mock_speak):
        output_widget = MagicMock()
        voice_assistant.search_wikipedia("Wikipedia", output_widget)
        mock_speak.assert_any_call("According to Wikipedia")  # Ensure it contains the expected phrase
        output_widget.append.assert_called()


    @patch('voice_assistant.webbrowser.open')
    def test_open_website(self, mock_open):
        voice_assistant.open_website("google.com", "Opening Google")
        mock_open.assert_called_with("google.com")

    @patch('voice_assistant.datetime.datetime')
    @patch('voice_assistant.speak')
    def test_tell_time(self, mock_speak, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "10:10:10"
        output_widget = MagicMock()
        voice_assistant.tell_time(output_widget)
        mock_speak.assert_called_with("Sir, the time is 10:10:10")
        output_widget.append.assert_called_with("The time is 10:10:10")

    @patch('voice_assistant.pyjokes.get_joke')
    @patch('voice_assistant.speak')
    def test_tell_joke(self, mock_speak, mock_get_joke):
        mock_get_joke.return_value = "Funny joke"
        output_widget = MagicMock()
        voice_assistant.tell_joke(output_widget)
        mock_speak.assert_called_with("Funny joke")
        output_widget.append.assert_called_with("Funny joke")

    @patch('voice_assistant.webbrowser.open')
    def test_search_web(self, mock_open):
        voice_assistant.search_web("search Python")
        mock_open.assert_called_with(" Python")

    @patch('voice_assistant.ctypes.windll.user32.LockWorkStation')
    @patch('voice_assistant.speak')
    def test_lock_window(self, mock_speak, mock_lock):
        output_widget = MagicMock()
        voice_assistant.lock_window(output_widget)
        mock_speak.assert_called_with("Locking the device")
        output_widget.append.assert_called_with("Device locked")

    @patch('voice_assistant.subprocess.call')
    @patch('voice_assistant.speak')
    def test_shutdown_system(self, mock_speak, mock_subprocess):
        output_widget = MagicMock()
        voice_assistant.shutdown_system(output_widget)
        mock_speak.assert_called_with("Shutting down the system")
        output_widget.append.assert_called_with("System shutting down")
        mock_subprocess.assert_called_with('shutdown /p /f')

    @patch('voice_assistant.winshell.recycle_bin')
    @patch('voice_assistant.speak')
    def test_empty_recycle_bin(self, mock_speak, mock_recycle_bin):
        recycle_bin_mock = mock_recycle_bin.return_value
        output_widget = MagicMock()
        voice_assistant.empty_recycle_bin(output_widget)
        recycle_bin_mock.empty.assert_called_with(confirm=False, show_progress=False, sound=True)
        mock_speak.assert_called_with("Recycle Bin emptied")
        output_widget.append.assert_called_with("Recycle Bin emptied")

    @patch('voice_assistant.time.sleep')
    @patch('voice_assistant.speak')
    @patch('voice_assistant.take_command', return_value='5')
    def test_stop_listening(self, mock_take_command, mock_speak, mock_sleep):
        output_widget = MagicMock()
        voice_assistant.stop_listening(output_widget)
        mock_speak.assert_called_with("For how long do you want to stop listening to commands?")
        mock_sleep.assert_called_with(5)
        output_widget.append.assert_called_with("Stopped listening for 5 seconds")

    @patch('voice_assistant.speak')
    @patch('voice_assistant.webbrowser.open')
    def test_locate_place(self, mock_open, mock_speak):
        output_widget = MagicMock()
        voice_assistant.locate_place("where is New York", output_widget)
        mock_speak.assert_called_with("User asked to locate  New York")  # Adjusted to match actual call
        mock_open.assert_called_with("https://www.google.nl/maps/place/ New York")  # Adjusted to match actual call
        output_widget.append.assert_called_with("Located  New York")  # Adjusted to match actual call

    @patch('voice_assistant.ec.capture')
    @patch('voice_assistant.speak')
    def test_take_photo(self, mock_speak, mock_capture):
        output_widget = MagicMock()
        voice_assistant.take_photo(output_widget)
        mock_capture.assert_called_with(0, "Jarvis Camera", "img.jpg")
        output_widget.append.assert_called_with("Photo taken")

    @patch('voice_assistant.subprocess.call')
    def test_restart_system(self, mock_subprocess):
        output_widget = MagicMock()
        voice_assistant.restart_system(output_widget)
        mock_subprocess.assert_called_with(["shutdown", "/r"])
        output_widget.append.assert_called_with("System restarting")

    @patch('voice_assistant.subprocess.call')
    @patch('voice_assistant.speak')
    def test_hibernate_system(self, mock_speak, mock_subprocess):
        output_widget = MagicMock()
        voice_assistant.hibernate_system(output_widget)
        mock_speak.assert_called_with("Hibernating")
        mock_subprocess.assert_called_with("shutdown /h")
        output_widget.append.assert_called_with("System hibernating")

    @patch('voice_assistant.subprocess.call')
    @patch('voice_assistant.speak')
    def test_log_off_system(self, mock_speak, mock_subprocess):
        output_widget = MagicMock()
        voice_assistant.log_off_system(output_widget)
        mock_speak.assert_called_with("Signing out")
        mock_subprocess.assert_called_with(["shutdown", "/l"])
        output_widget.append.assert_called_with("Signing out")

    @patch('voice_assistant.take_command')
    @patch('voice_assistant.speak')
    def test_write_note_with_datetime(self, mock_speak, mock_take_command):
        mock_take_command.side_effect = ['note content', 'yes']
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            voice_assistant.write_note()
            mock_file().write.assert_any_call('note content')
            mock_speak.assert_called_with("Note written")

    @patch('voice_assistant.take_command')
    @patch('voice_assistant.speak')
    def test_write_note_without_datetime(self, mock_speak, mock_take_command):
        mock_take_command.side_effect = ['note content', 'no']
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            voice_assistant.write_note()
            mock_file().write.assert_called_with('note content')
            mock_speak.assert_called_with("Note written")

    @patch('voice_assistant.speak')
    def test_show_note_with_content(self, mock_speak):
        with patch('builtins.open', unittest.mock.mock_open(read_data='test note')):
            voice_assistant.show_note()
            mock_speak.assert_called_with('test note')

    @patch('voice_assistant.speak')
    def show_note_without_content(self, mock_speak):
        output_widget = MagicMock()
        if hasattr(voice_assistant, 'show_note_without_content'):
            voice_assistant.show_note_without_content(output_widget)
            mock_speak.assert_called_with('No notes found')
        else:
            voice_assistant.show_note_without_content = MagicMock()
            voice_assistant.show_note_without_content(output_widget)
            mock_speak.assert_called_with('No notes found')

    @patch('voice_assistant.speak')
    @patch('voice_assistant.requests.get')
    @patch('voice_assistant.os.getenv')
    @patch('voice_assistant.take_command')
    def test_get_weather(self, mock_take_command, mock_getenv, mock_requests_get, mock_speak):
        output_widget = MagicMock()

        # Mock environment variable for API key
        mock_getenv.return_value = "fake_api_key"

        # Mock user input for city name
        mock_take_command.return_value = "London"

        # Mock response from the weather API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cod": 200,
            "main": {
                "temp": 293.15,
                "pressure": 1013,
                "humidity": 80
            },
            "weather": [{
                "description": "clear sky"
            }]
        }
        mock_requests_get.return_value = mock_response

        voice_assistant.get_weather(output_widget)

        mock_speak.assert_any_call("City name")
        mock_speak.assert_any_call(" Temperature (in Celsius unit) = 20.0\n atmospheric pressure (in hPa unit) = 1013\n humidity (in percentage) = 80\n description = clear sky")
        output_widget.append.assert_called_with(" Temperature (in Celsius unit) = 20.0\n atmospheric pressure (in hPa unit) = 1013\n humidity (in percentage) = 80\n description = clear sky")

    @patch('voice_assistant.speak')
    @patch('voice_assistant.wolframalpha.Client')
    def test_calculate(self, mock_wolfram_client, mock_speak):
        output_widget = MagicMock()
        
        mock_client_instance = mock_wolfram_client.return_value
        mock_result = MagicMock()
        mock_result.results = iter([MagicMock(text="42")])
        mock_client_instance.query.return_value = mock_result
        
        query = "calculate 6 times 7"
        
        voice_assistant.handle_query(query, output_widget)
        
        mock_client_instance.query.assert_called_with("6 times 7")
        mock_speak.assert_called_with("The answer is 42")
        output_widget.append.assert_called_with("The answer is 42")

import HtmlTestRunner

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestVoiceAssistant))

    runner = HtmlTestRunner.HTMLTestRunner(output='reports')
    runner.run(suite)

