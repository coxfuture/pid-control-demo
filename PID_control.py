import pygame
import math

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()



# Set up the display
display_x = 1000
display_y = 1000
screen = pygame.display.set_mode((display_x, display_y))

# Define the ball's properties
ball_x = 500
ball_y = 500
ball_radius = 20
ball_color = (255, 10, 16)
ball_speed_x = 0
ball_speed_y = 0

error_x = 0
error_y = 0

#pid values
kp = 0.0001
ki = 0.00000000001
kd = 0.0001

# Initialize the error, integral, and derivative terms
error_x = 0
error_y = 0
integral_x = 0
integral_y = 0
derivative_x = 0
derivative_y = 0
previous_error_x = 0
previous_error_y = 0
pid = 0 
cum_error_x = 0
cum_error_y = 0

# Define constants
gravity = 0.000981
friction = 0.01
ball_mass = 1

# Define the font and color for the framerate display
font = pygame.font.Font(None, 30)
color = (255, 255, 255)

def movetomouse(ball_speed_y,ball_speed_x):



    return int(ball_speed_x), int(ball_speed_y)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball_speed_y -= 0.5
            elif event.key == pygame.K_DOWN:
                ball_speed_y += 0.5
            elif event.key == pygame.K_LEFT:
                ball_speed_x -= 0.5
            elif event.key == pygame.K_RIGHT:
                ball_speed_x += 0.5
            elif event.key == pygame.K_F1:
                kp = kp * 0.8
            elif event.key == pygame.K_F2:
                kp = kp * 1.2   
            elif event.key == pygame.K_F3:
                ki = ki * 0.8
            elif event.key == pygame.K_F4:
                ki = ki * 1.2   
            elif event.key == pygame.K_F5:
                kd = kd * 0.8
            elif event.key == pygame.K_F6:
                kd = kd * 1.2   
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Start moving the ball to the mouse cursor
            pid = 1 
        if event.type == pygame.MOUSEBUTTONUP:
            # Stop moving the ball
            pid = 0 
            error_x = 0
            error_y = 0
            integral_x = 0
            integral_y = 0
            derivative_x = 0
            derivative_y = 0
            cum_error_x = 0
            cum_error_y = 0
    elapsed_time = clock.tick(60)
    # Update the ball position and speed
    if pid == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        error_x = mouse_x - ball_x
        error_y = mouse_y - ball_y
        if error_x != 0 or error_y != 0:
            
            # Update the integral term
            cum_error_x += error_x
            cum_error_y += error_y
            integral_x += cum_error_x * elapsed_time
            integral_y += cum_error_y * elapsed_time

            # Update the derivative term
            derivative_x = (error_x - previous_error_x) / elapsed_time
            derivative_y = (error_y - previous_error_y) / elapsed_time
            previous_error_x = error_x
            previous_error_y = error_y


            # Calculate the speed using the PID formula
            ball_speed_x += kp * error_x + ki * integral_x + kd * derivative_x
            ball_speed_y += kp * error_y + ki * integral_y + kd * derivative_y

    # Update the ball position
    ball_x += ((ball_speed_x - friction)* elapsed_time) 
    ball_y += ((ball_speed_y - friction)* elapsed_time) 


    # Apply gravity to the ball's speed
    ball_speed_y += gravity
    print(derivative_x)

    
    # Bounce the ball when it hits the bottom of the screen
    if ball_y + ball_radius >= 1000:
        ball_y = 1000 - ball_radius
        ball_speed_y = -ball_speed_y * 0.8

    if ball_x + ball_radius >= 1000:
        ball_x = 1000 - ball_radius
        ball_speed_x = -ball_speed_x * 0.8

    if ball_y - ball_radius <= 0:
        ball_y = 0 + ball_radius
        ball_speed_y = -ball_speed_y * 0.8
        
    if ball_x - ball_radius <= 0:
        ball_x = 0 + ball_radius
        ball_speed_x = -ball_speed_x * 0.8

    # Clear the screen
    screen.fill((200, 200, 200))

    
    fps = int(clock.get_fps())
    text = font.render(str(fps), True, color)
    screen.blit(text, (10, 10))
    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    d_term_hist = []
    d_term_hist.append(derivative_x)
    if len(d_term_hist) > 1000:
        d_term_hist.pop(0)
    for index, d in enumerate(d_term_hist):
        dot_pos_x = display_x - index
        pygame.draw.circle(screen, (0,0,255), (display_y - 1000 * derivative_x, dot_pos_x), 5)


    #draw proportional force in red
    pygame.draw.line(screen, (255,0,0), start_pos=(ball_x,ball_y), end_pos=(ball_x + error_x, ball_y))
    pygame.draw.line(screen, (255,0,0), start_pos=(ball_x,ball_y), end_pos=(ball_x,ball_y + error_y))
    
    #draw integral force in green 
    pygame.draw.line(screen, (0,255,0), start_pos=(ball_x,ball_y), end_pos=(ball_x + 100000*integral_x*ki, ball_y))
    pygame.draw.line(screen, (0,255,0), start_pos=(ball_x,ball_y), end_pos=(ball_x, ball_y + 100000*integral_y*ki))
    
    #draw derivative force in blue
    pygame.draw.line(screen, (0,0,255), start_pos=(ball_x,ball_y), end_pos=(ball_x + 1000*derivative_x*kd, ball_y))
    pygame.draw.line(screen, (0,0,255), start_pos=(ball_x,ball_y), end_pos=(ball_x, ball_y + 1000*derivative_y*kd))

    text = font.render("x: " + str(math.trunc(ball_x)), True, color)
    screen.blit(text, (ball_x, ball_y))
    text = font.render("y: " + str(math.trunc(ball_y)), True, color)
    screen.blit(text, (ball_x, ball_y - 20))
    
    #render legend
    text = font.render("Proportional (F1/F2 to adjust): " + str(kp), True, (255,0,0))
    screen.blit(text, (10,40))
    text = font.render("Integral (F2/F3 to adjust): " + str(ki), True, (0,255,0))
    screen.blit(text, (10,60))
    text = font.render("Derivative (F4/F5 to adjust): " + str(kd), True, (0,0,255))
    screen.blit(text, (10,80))
    #Update the display
    pygame.display.update()


# Quit Pygame
pygame.quit()