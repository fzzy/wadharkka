model = { name: "Jonas" }
element = Serenade.view('h1 "Hello " @name').render(model)
document.getElementById("content").appendChild(element)