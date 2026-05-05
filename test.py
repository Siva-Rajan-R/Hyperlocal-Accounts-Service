class Hello():
    def __init__(self, name:str):
        self.name = name

    def say_hello(self):
        return f"Hello {self.name}!"
    

if not getattr(Hello(name="hello"),"say_hello"):
    print("Method exists")