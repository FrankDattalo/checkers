import multiprocessing
import policynetplayer
import game
import utils

class ParentPolicyNetPlayer(policynetplayer.PolicyNetPlayer):

    def __init__(self, save_interval, total_games, update_interval=25, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = multiprocessing.Queue()
        self._child_queues = []
        self._save_interval = save_interval
        self._num_training_steps_since_last_save = 0
        self._total_games = total_games
        self._current_game_count = 0
        self._timer = utils.Timer()
        self._update_interval = update_interval
        self._total_loss = 0
        self._total_trained = 0


    def recieve_and_handle(self):
        message_type, contents, child_queue_index = self._queue.get(True)
        child_queue = self._child_queues[child_queue_index]
        result = self.handle(message_type, contents)
        child_queue.put(result)


    def handle(self, message_type, contents):

        if message_type == 'train':
            num_samples = len(contents[0])          
            loss = self._train(contents[0], contents[1], verbose=0)
            total_loss = loss * num_samples
            self._total_loss += total_loss
            self._total_trained += num_samples

            if self._num_training_steps_since_last_save >= self._save_interval:
                print('Saving...')
                self._save()
                print('Done saving!')
                self._num_training_steps_since_last_save = 0
            else:
                self._num_training_steps_since_last_save += 1

            self._current_game_count += 1

            if self._current_game_count % self._update_interval == 0:
                eta = self._timer.eta(self._current_game_count, self._total_games)
                print('Progress: {}/{}, Average Loss: {}, {}'.format(
                    self._current_game_count, self._total_games, self._total_loss / self._total_trained, eta))

        elif message_type == 'predict':
            return self._pred(contents)

        else:
            raise Exception('Unknown message type: {}'.format(message_type))


    def spawn(self):
        queue_index = len(self._child_queues)
        child_queue = multiprocessing.Queue()
        self._child_queues.append(child_queue)
        child = ChildPolicyNetPlayer(self._queue, queue_index, child_queue)
        return child
        


class ChildPolicyNetPlayer(policynetplayer.PolicyNetPlayer):
    
    def __init__(self, parent_queue, queue_index, child_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_queue = parent_queue
        self._queue_index = queue_index
        self._queue = child_queue

    def start(self):
        self._history = []

    def end(self):
        pass

    def _train(self, X, y):
        return self._message_parent('train', (X, y))

    def _pred(self, X):
        return self._message_parent('predict', X)

    def _save(self):
        pass

    def _message_parent(self, message_type, contents):
        self._parent_queue.put((message_type, contents, self._queue_index), True)
        result = self._queue.get(True)
        return result


def child_process_fn(p1, p2, games):
    g = game.Game(p1, p2, display=False, delay=None)
    for _ in range(games):
        g.run()



def main():
    num_children_processes = 11
    num_games_per_process = 100_000
    save_interval = 100

    total_games = num_games_per_process * num_children_processes

    parent_player = ParentPolicyNetPlayer(save_interval, total_games, 
        file_name='policynet-75x500.h5', hidden_layers=75, hidden_layer_size=500)
    child_processes = []

    def child_process_is_alive():
        nonlocal child_processes
        for c in child_processes:
            if c.is_alive():
                return True
        return False

    # spawns the children processes from the one parent process
    for _ in range(num_children_processes):
        p1 = parent_player.spawn()
        p2 = parent_player.spawn()

        child_process = multiprocessing.Process(
            target=child_process_fn, args=(p1, p2, num_games_per_process))

        child_processes.append(child_process)
        child_process.start()
    
    parent_player.start()

    while child_process_is_alive():
        parent_player.recieve_and_handle()

    parent_player.end()


if __name__ == '__main__':
    main()