import numpy as np
import random
from collections import deque
import pygame

pygame.init()

WIDTH,HEIGHT = 1000,1000
Maze_Size = 128*2

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
visited = {start}
queue = deque([start])
parents = {}


rows,cols = maze.shape

grid_size = maze.shape[0]

Cell_Size = WIDTH / grid_size
offset = (1000 - grid_size * Cell_Size) // 2
found_end = False

path = []

visited_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

def algorithm():
    curx, cury = queue.popleft()
    
    for dx, dy in directions:
        x,y = curx,cury
        if curx+dx > 0:
           x = curx+dx
        if cury+dy > 0:
            y = cury+dy
        
        

        if maze[y][x] == 0 and (x,y) not in visited:
            
            queue.append((x,y))
            visited.add((x,y))
            pygame.draw.rect(
                visited_surface,
                (207,147,147),
                pygame.Rect(
                    int(x * Cell_Size + offset),
                    int(y * Cell_Size + offset),
                    Cell_Size,
                    Cell_Size
                )
            )

            parents[(x,y)] = (curx,cury)
        
        if (x,y) == end:
            global found_end
            visited.add((x,y))
            current = end
            while current != start:
                path.append(current)
                current = parents[current]
            
            path.append(start)
            path.reverse()
            found_end = True
            break
            

                
maze_surface = pygame.Surface((WIDTH, HEIGHT))

maze_surface.fill((255, 255, 255))

for y in range(rows):
    for x in range(cols):
        if maze[y][x] == 1:
            pygame.draw.rect(
                maze_surface,
                (0, 0, 0),
                pygame.Rect(
                    int(x * Cell_Size + offset),
                    int(y * Cell_Size + offset),
                    Cell_Size,
                    Cell_Size
                )
            )

lasttick = pygame.time.get_ticks()
interval = 0

while True:
    curtick = pygame.time.get_ticks()
    if curtick-lasttick >= interval:
        for _ in range(100):
            if not found_end:
                algorithm()

    screen.blit(maze_surface, (0,0))
    screen.blit(visited_surface, (0,0))

    for x, y in path:
        pygame.draw.rect(
            screen,
            (245, 230, 100),
            pygame.Rect(
                int(x * Cell_Size + offset),
                int(y * Cell_Size + offset),
                Cell_Size,
                Cell_Size
            )
        )

    pygame.draw.rect(
        screen,
        (100, 255, 100),
        pygame.Rect(
            int(start[0] * Cell_Size + offset),
            int(start[1] * Cell_Size + offset),
            Cell_Size,
            Cell_Size
        )
    )

    pygame.draw.rect(
        screen,
        (100, 100, 255),
        pygame.Rect(
            int(end[0] * Cell_Size + offset),
            int(end[1] * Cell_Size + offset),
            Cell_Size,
            Cell_Size
        )
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.flip()