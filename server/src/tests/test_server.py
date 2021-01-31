import unittest
from handles import UserAction, CommandAction


class UserActionTestCase(unittest.TestCase):
    def setUp(self):
        self.user_action = UserAction()

    def test_get_user_msg(self):
        message = 'test message'
        one_user_msg = self.user_action.getUserMsg(payload=f'@user1 {message}')
        self.assertEqual(one_user_msg, message)

        many_users_msg = self.user_action.getUserMsg(
            payload=f'@user1,@user2,@user3 {message}')
        self.assertEqual(many_users_msg, message)

        all_users_msg = self.user_action.getUserMsg(payload=f'{message}')
        self.assertEqual(all_users_msg, message)

    def test_fetch_users(self):
        message = 'test message'
        one_user = self.user_action.fetchUsers(payload=f'@user1 {message}')
        self.assertEqual(one_user, ['user1'])

        many_users = self.user_action.fetchUsers(
            payload=f'@user1,@user2,@user3 {message}')
        self.assertEqual(many_users, ['user1', 'user2', 'user3'])

        none_user = self.user_action.fetchUsers(payload=f'{message}')
        self.assertEqual(none_user, None)


class ChatCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.command_action = CommandAction()

    def test_fetch_command_userlist(self):
        command = '/userlist'
        message = f'{command}'
        cmd = self.command_action.fetchCommand(message)
        self.assertEqual(cmd, command)

        message = f'{command} test msg'
        cmd = self.command_action.fetchCommand(message)
        self.assertEqual(cmd, command)

        message = f'test msg'
        cmd = self.command_action.fetchCommand(message)
        self.assertEqual(cmd, None)

    def test_userlist_is_command(self):
        command = '/userlist'
        message = f'{command}'
        result = self.command_action.is_command(message)
        self.assertTrue(result)

        message = f'{command} test msg'
        result = self.command_action.fetchCommand(message)
        self.assertTrue(result)

        message = f'test msg'
        result = self.command_action.fetchCommand(message)
        self.assertFalse(result)

    def test_get_command_params(self):
        command = '/nickname'
        param = 'user1'
        message = f'{command} {param}'
        result = self.command_action.getCommandParams(message)
        self.assertEqual(result, param)
