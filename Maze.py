import numpy as np
import random
from collections import deque
import pygame

pygame.init()

WIDTH,HEIGHT = 600,600
Maze_Size = 16

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze_Algorithm")

directions = [(0,1),(1,0),(0,-1),(-1,0)]

def create_maze(dim):
    maze = np.ones((dim*2+1,dim*2+1))

    x,y = (0,0)
    maze[2*x+1,2*y+1] = 0
    
    stack = [(x,y)]
    while len(stack) > 0:
        x, y = stack[-1]

        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] ==1:
                maze[2*nx+1, 2*ny+1] = 0
                maze[2*x+1+dx, 2*y+1+dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    
    maze[1,0] = 0
    maze[-2,-1] = 0

    return maze

maze = create_maze(Maze_Size)


start = (0,1)
end = (maze.shape[0]-2, maze.shape[1]-2)
visited = [start]
queue = [start]
parents = {}


rows,cols = maze.shape

grid_size = maze.shape[0]

Cell_Size = min(600 // grid_size, 600 // grid_size)
offset = (600 - grid_size * Cell_Size) // 2
found_end = False

path = []

def algorithm():
    curx,cury = queue.pop(0)
    print(curx,cury)
    for dx, dy in directions:
        x,y = curx,cury
        if curx+dx > 0:
           x = curx+dx
        if cury+dy > 0:
            y = cury+dy
        
        

        if maze[y][x] == 0 and not ((x,y) in visited):
            
            queue.append((x,y))
            visited.append((x,y))

            parents[(x,y)] = (curx,cury)
        
        if (x,y) == end:
            global found_end
            visited.append((x,y))
            current = end
            while current != start:
                path.append(current)
                current = parents[current]
            
            path.append(start)
            path.reverse()
            found_end = True
            print(path)
            break
            

last_time = pygame.time.get_ticks()
interval = 1

while True:

    current_time = pygame.time.get_ticks()

    if current_time-last_time >= interval:
        last_time = current_time
        bot_x = 1
        if not found_end:
            algorithm()

    screen.fill((255,255,255))
    for y in range(rows):
        for x in range(cols):
                for p_x,p_y in path:
                    if x == p_x and y == p_y:
                        pygame.draw.rect(screen,(245, 230, 100),pygame.Rect(
                        int(x * Cell_Size + offset),
                        int(y * Cell_Size + offset),
                        Cell_Size,
                        Cell_Size
                                                                      ),0) 
                
                for q_x,q_y in visited:
                    if x==q_x and y==q_y and not ((x,y) in path):
                       pygame.draw.rect(screen,(207, 147, 147),pygame.Rect(
                        int(x * Cell_Size + offset),
                        int(y * Cell_Size + offset),
                        Cell_Size,
                        Cell_Size
                                                                      ),0) 

                if maze[y][x] == 1:
                    pygame.draw.rect(screen,(0,0,0),pygame.Rect(
                        int(x * Cell_Size + offset),
                        int(y * Cell_Size + offset),
                        Cell_Size,
                        Cell_Size
                                                                      ),0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    pygame.display.flip()