from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

class todo(BaseModel):
    progress: str
    activity: str

class update(BaseModel):
    progress: Optional[str]=None
    activity: Optional[str]=None

todolist = {
    1: todo(progress="On Going", activity="Walk the dog"),
    2: todo(progress="Completed", activity="Water the flowers")
}

#GET
@app.get("/get-todo/{id}")
def get_todos(id: int = Path(description="ID of activity")):
    return todolist[id]

@app.get("/get-by-title/{title}")
def get_by_title(title:str):
    for activity_id in todolist:
        if todolist[activity_id].activity == title:
            return todolist[activity_id]
        else:
            return {"activity does not exist"}
        
#POST
@app.post("/create-todo/{activity_id}")
def add_todos(activity_id:int, todos: todo):

    if activity_id in todolist:
        return {"todo already exists"}
    
    todolist[activity_id] = todos
    return todolist[activity_id]

#PUT
@app.put("/update-todo/{activity_id}")
def update_todos(activity_id: int, todos: update):

    if activity_id not in todolist:
        return {"activity does not exist"} 
    
    if todos.progress != None:
        todolist[activity_id].progress = todos.progress

    if todos.activity != None:
        todolist[activity_id].activity = todos.activity
        
    return todos[activity_id]

#DELETE
@app.delete("/delete-todo/{activity_id}")
def delete_todos(activity_id: int):
    if activity_id not in todolist:
        return {"activity does not exist"}
    else:
        del todolist[activity_id]
    return {"activity successfully deleted"} 