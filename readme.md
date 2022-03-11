O novo modelo é baseado no modelo "Forest fire", com a adição de uma nova condição da árvore, "úmida", em que se dificulta a queima da floresta.

A hipótese em questão é de que com a floresta úmida a dificuldade de queimar é maior, com isso foi adicionado a opção de escolher a porcentagem de árvores úmidas no modelo, sendo que cada arvore úmida tem uma chance de 25% de voltar a secar e pegar fogo caso o foco ainda esteja próximo. Com base na porcentagem escolhida, o modelo gera as árvores úmidas aleatoriamente, com o seguinte código:

count = 1
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                count += 1
        quantity = count * (humidity_level)
        randomX = self.random.sample(range(count), int(quantity))
        randomY = self.random.sample(range(count), int(quantity))
        randomX.sort()
        randomY.sort()
        ##
        # Place a tree in each cell with Prob = density
        count = 0
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                if x in randomX and x != 0:
                    if y in randomY:
                        new_tree.condition = "Humid"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

E para determinar se a árvore pega fogo ou não, em todo passo é gerado um numero aleatorio de 0 até 3, o que determina 25% de chance de árvore voltar a pegar fogo.

if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
                if neighbor.condition == "Humid":
                    number = self.random.randint(0,3)
                    if number == 0:
                        neighbor.condition = "Fine"
            self.condition = "Burned Out"


O arquivo CSV gerado contém as seguintes variáveis:

,density,humidity_level,Run,Burned Out,Fine,Fire,Humid,height,width

Sendo respectivamente a densidade do modelo, a porcentagem de árvores úmidas, qual o passo da execução, quantidade de árvores totalmente queimadas, quantidade de árvores normais, quantidade de árvores em chamas, quantidade de árvores umidas, e a altura e largura do modelo.

Segue abaixo as explicações originais de como utilizar o modelo:

# Forest Fire Model

## Summary

The [forest fire model](http://en.wikipedia.org/wiki/Forest-fire_model) is a simple, cellular automaton simulation of a fire spreading through a forest. The forest is a grid of cells, each of which can either be empty or contain a tree. Trees can be unburned, on fire, or burned. The fire spreads from every on-fire tree to unburned neighbors; the on-fire tree then becomes burned. This continues until the fire dies out.

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

To view and run the model analyses, use the ``Forest Fire Model`` Notebook.

## Files

### ``forest_fire/model.py``

This defines the model. There is one agent class, **TreeCell**. Each TreeCell object which has (x, y) coordinates on the grid, and its condition is *Fine* by default. Every step, if the tree's condition is *On Fire*, it spreads the fire to any *Fine* trees in its [Von Neumann neighborhood](http://en.wikipedia.org/wiki/Von_Neumann_neighborhood) before changing its own condition to *Burned Out*.

The **ForestFire** class is the model container. It is instantiated with width and height parameters which define the grid size, and density, which is the probability of any given cell having a tree in it. When a new model is instantiated, cells are randomly filled with trees with probability equal to density. All the trees in the left-hand column (x=0) are set to *On Fire*.

Each step of the model, trees are activated in random order, spreading the fire and burning out. This continues until there are no more trees on fire -- the fire has completely burned out.


### ``forest_fire/server.py``

This code defines and launches the in-browser visualization for the ForestFire model. It includes the **forest_fire_draw** method, which takes a TreeCell object as an argument and turns it into a portrayal to be drawn in the browser. Each tree is drawn as a rectangle filling the entire cell, with a color based on its condition. *Fine* trees are green, *On Fire* trees red, and *Burned Out* trees are black.

## Further Reading

Read about the Forest Fire model on Wikipedia: http://en.wikipedia.org/wiki/Forest-fire_model

This is directly based on the comparable NetLogo model:

Wilensky, U. (1997). NetLogo Fire model. http://ccl.northwestern.edu/netlogo/models/Fire. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

