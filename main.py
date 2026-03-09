#base component class
class Panel:
    def display(self):
        raise NotImplementedError  #note: this is a placeholder class. Its basically saying every panel needs to have a display() method but it gets defined when you inherit from it!

class Button:
    def display(self):
        raise NotImplementedError

class Textbox:
    def display(self):
        raise NotImplementedError


#word90 components
class Word90Panel(Panel):
    def display(self):  #its own version of display panel
        return "Panel Word90"

class Word90Button(Button):
    def display(self):  #its own version of display button
        return "Button Word90"

class Word90Textbox(Textbox):
    def display(self):  #its own version of display textbox
        return "Textbox Word90"


#word00 components
class Word00Panel(Panel):
    def display(self):
        return "Panel Word00"

class Word00Button(Button):
    def display(self):
        return "Button Word00"

class Word00Textbox(Textbox):
    def display(self):
        return "Textbox Word00"


#word10 components
class Word10Panel(Panel):
    def display(self):
        return "Panel Word10"

class Word10Button(Button):
    def display(self):
        return "Button Word10"

class Word10Textbox(Textbox):
    def display(self):
        return "Textbox Word10"


#word21 components
class Word21Panel(Panel):
    def display(self):
        return "Panel Word21"

class Word21Button(Button):
    def display(self):
        return "Button Word21"

class Word21Textbox(Textbox):
    def display(self):
        return "Textbox Word21"


#abstract factory base that basically says every factory must have these 3 methods
class GenerationFactory:
    def make_panel(self):
        raise NotImplementedError

    def make_button(self):
        raise NotImplementedError

    def make_textbox(self):
        raise NotImplementedError


#singleton rule
# tracks how many times each generation has been used this run and blocks anything over 2.
class LimitedFactory(GenerationFactory):
    usage_tracker = {}  #tracks count per factory
    LIMIT = 2

    @classmethod
    def request(cls):
        #chatGPT: how to get specific subclass in python
        label = cls.__name__  #gets the name of whatever subclass is calling it
        times_used = cls.usage_tracker.get(label, 0) #looks up the name of the factory in the dictionary. If the key doesn't exist, return 0

        if times_used >= cls.LIMIT:  #if count is 2 or more, send a warning message
            print(f"  WARNING: {label} has already run {cls.LIMIT} times. Skipping this entry.")
            return None

        cls.usage_tracker[label] = times_used + 1  #if under the limit then increment the count
        return cls()

    @classmethod  #clears the dictionary so we can reset to zero for each test run
    def clear_tracker(cls):
        cls.usage_tracker.clear()


#concrete factories
class FactoryWord90(LimitedFactory):
    def make_panel(self):   return Word90Panel()
    def make_button(self):  return Word90Button()
    def make_textbox(self): return Word90Textbox()

class FactoryWord00(LimitedFactory):
    def make_panel(self):   return Word00Panel()
    def make_button(self):  return Word00Button()
    def make_textbox(self): return Word00Textbox()

class FactoryWord10(LimitedFactory):
    def make_panel(self):   return Word10Panel()
    def make_button(self):  return Word10Button()
    def make_textbox(self): return Word10Textbox()

class FactoryWord21(LimitedFactory):
    def make_panel(self):   return Word21Panel()
    def make_button(self):  return Word21Button()
    def make_textbox(self): return Word21Textbox()


#maps generation names from the file to factory classes
generation_lookup = {
    "Word90": FactoryWord90,
    "Word00": FactoryWord00,
    "Word10": FactoryWord10,
    "Word21": FactoryWord21,
}

# main test
def run_gui_tests(filepath):
    LimitedFactory.clear_tracker()

    #chatGPT: how to read file into a list
    with open(filepath) as f:
        entries = [line.strip() for line in f if line.strip()]

    print("  MicroOffice GUI Test Run")
    for entry in entries:
        target = generation_lookup.get(entry)  #checks which factory it is

        if target is None:
            print(f"  Unknown generation: {entry} — skipping.")
            continue

        factory = target.request()  #requests an instance
        if factory is None:
            continue

        #use the factory to display each component
        print(f"\n  Testing {entry}:")
        print(f"    {factory.make_panel().display()}")
        print(f"    {factory.make_button().display()}")
        print(f"    {factory.make_textbox().display()}")

    print("  Done.")

run_gui_tests("config.txt")
