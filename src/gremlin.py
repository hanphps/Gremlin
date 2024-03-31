# Author: Hannah (@github: hanphps)
import time

class Event:

    def __init__(self,
                 task : str = '',
                 msg : str = '',
                 blocking : bool = False):
        
        self.task = task
        self.msg = msg
        self.timestamp = time.time()
        self.blocking = blocking

        # Doubly linked for accessibility
        self.previous = None
        self.next = None

class Gremlin:
    def __init__(self, 
                 hndl : str = ''):
        self.handle = hndl
        self.curr_evt = None
    
    def link_event(self,
                   task: str,
                   msg : str,
                   blocking : bool = False):
        warning = '(%s) > [EVENT]: Linking event (task = {%s}, msg = {%s}, blocking = {%s})' % (time.time(),task,msg,blocking)
        print(warning)
        evt = Event(task=task, msg=msg, blocking=blocking)
        if evt is not None:
            if self.curr_evt != None:
                if self.curr_evt.next == None:
                    evt.previous = self.curr_evt
                    self.curr_evt.next = evt
                    self.curr_evt = self.curr_evt.next
                else:
                    curr_evt = self.curr_evt
                    while curr_evt.next != None:
                        curr_evt = curr_evt.next
                    
                    curr_evt.next = evt
                    self.curr_evt = curr_evt.nxt
            else:
                self.curr_evt = evt
            
            if evt.blocking :
                self.hndl_error(self.curr_evt)
        else:
            raise Exception('Event does not exist!')

    def link_error(self,
                   task : str = 'unknown',
                   msg : str = 'unknown'):
        self.link_event(task=task, msg=msg, blocking=True)

    def hndl_error(self,
                   evt: Event):
        warning = '(%s) > [EVENT]: Handling error event (task = {%s}, msg = {%s}, blocking = {%s})' % (time.time(),evt.task,evt.msg,evt.blocking)
        print(warning)
        has_blocking        = False
        first_blocking_msg  = ''
        if evt is not None:
            curr_evt = evt
            while curr_evt.previous != None:
                # TODO: callback events
                #if curr_evt.callback is not None:
                #        curr_evt.callback()
                warning = '(%s) > [EVENT]: Previous event (task = {%s}, msg = {%s}, blocking = {%s})' % (time.time(),curr_evt.task,curr_evt.msg,curr_evt.blocking)
                print(warning)
                if curr_evt.blocking and not has_blocking:
                    # This should be root error however it can be blocked because of previous unknown issues
                    has_blocking = True
                    first_blocking_msg = curr_evt.msg

                curr_evt = curr_evt.previous
            
            # TODO: callback events
            #if curr_evt.callback is not None:
            #        curr_evt.callback()
            
            warning = '(%s) > [EVENT]: Previous event (task = {%s}, msg = {%s}, blocking = {%s})' % (time.time(),curr_evt.task,curr_evt.msg,curr_evt.blocking)
            print(warning)

            # Raise first blocking error
            if has_blocking:
                raise Exception(first_blocking_msg)
            self.curr_evt = None
        else:
            raise Exception('Event does not exist!')

    #TODO
    def dump_evt_log(self):
        pass