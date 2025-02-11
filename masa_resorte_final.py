from manim import *
import numpy as np

class Masa_resorte(Scene):
    def construct(self):
        self.camera.background_color = WHITE  
        #-----------------------------------------------#
        # 1) PRIMERA PARTE: Animación Movimiento Sin Amortiguamiento
        #-----------------------------------------------#



        titulo_grafico = Tex("The Mass-Spring Oscillator", color= DARK_BLUE)
        titulo_grafico.to_edge(UP)
        self.play(Write(titulo_grafico))
        self.wait(1)  # lo dejas un segundo visible

         # Create axes with dark blue axes lines
        grafica = Axes(
            x_range=[0, 9, 1], 
            y_range=[-1, 1.5, 0.5],
            axis_config={"color": DARK_BLUE},  # color for the axis lines
            tips=True
        ).scale(0.5)
        grafica.to_edge(LEFT)
        grafica.shift(RIGHT * 0.5) 

        
        # Add numerical labels (coordinate labels) along each axis
        grafica.add_coordinates().scale(0.8)
        
        # Grab the coordinate label group and set it to dark blue
        coordinate_labels = grafica.get_coordinate_labels()
        coordinate_labels.set_color(DARK_BLUE)
        label_x = MathTex(r"t \, \text{sec}", color = DARK_BLUE).scale(0.8)  # Reduce tamaño de la etiqueta
        label_y = MathTex(r"x \, \text{cm}", color = DARK_BLUE).scale(0.8)  # Reduce tamaño de la etiqueta
        label_x.move_to(grafica.coords_to_point(9, -0.5))
        label_y.move_to(grafica.coords_to_point(-0.9,1.5))

        # Grab the coordinate label group and set it to dark blue
        coordinate_labels = grafica.get_coordinate_labels()
        coordinate_labels.set_color(DARK_BLUE)

        
        # Parámetros del sistema (primer sistema)
        SHIFT_MASA_1 = 10 * RIGHT   # Desplaza la masa en la escena
        A1, w1, epsilon1 = 1, 3, 0  # Amplitud y frecuencia (sin amortiguamiento)
        
        # Parámetro de tiempo
        tiempo = ValueTracker(0)

        # Masa y anclaje (primer sistema)
        masa1 = Rectangle(width=0.8, height=0.4, color=BLUE, fill_opacity=1)
        masa1.move_to(grafica.c2p(0, 0) + SHIFT_MASA_1)
        
        anclaje_coord_1 = grafica.c2p(0, 1.5) + SHIFT_MASA_1
        dibujo_anclaje_1 = Rectangle(width=1, height=0.1, color=DARK_GRAY, fill_opacity=0.9)
        dibujo_anclaje_1.move_to(anclaje_coord_1)
        

 
        # Funciones de movimiento
        def calculo_amplitud_1(t):
            return A1 * np.exp(-epsilon1*t) * np.sin(w1 * t)

        def actualizar_masa_1(m):
            t = tiempo.get_value()
            # y(t) según la ecuación de masa1
            m.move_to(grafica.c2p(0, calculo_amplitud_1(t)) + SHIFT_MASA_1)
        # # Trayectoria masa 2
        trayectoria_1 = VGroup()
        def actualizar_trayectoria_1(tray):
            t = tiempo.get_value()
            y = calculo_amplitud_1(t)
            tray.add(
                Dot(
                    grafica.c2p(t, y),
                    radius=0.03,
                    color=BLUE
                )
            )
        trayectoria_1.add_updater(actualizar_trayectoria_1)



        # Para el resorte, creamos una "línea" con forma de resorte
        # (aquí se muestra un método muy simplificado)
        # Parámetros de la cicloide
        a, k = 0.05, 2

        def actualizar_cicloide(desf_trans=0):
            t = np.linspace(0, 18, 100)
            y_masa = masa1.get_center()[1]
            return VMobject().set_points_as_corners([
                grafica.c2p(a * (1 - k * np.cos(ti)), np.interp(ti, [0, 18], [anclaje_coord_1[1]+0.3, y_masa+0.4])) + SHIFT_MASA_1 + RIGHT*desf_trans
                for ti in t
            ]).set_color(GRAY)
        
        resorte_1 = always_redraw(actualizar_cicloide)       

        # Línea de referencia en x(t)
        ref_masa_1 = always_redraw(
            lambda: DashedLine(
                [grafica.c2p(tiempo.get_value(), 0)[0], masa1.get_center()[1], 0],
                masa1.get_center(), 
                color=BLUE
            )
        )

        # Activamos los updaters
        masa1.add_updater(actualizar_masa_1)
    
        # Agregamos a la escena
        self.play(Create(grafica), run_time=0.5)  # Dibuja la gráfica en 2 segundos
        # trayectoria_1.add_updater(actualizar_trayectoria_1)
        self.play(Write(label_x), Write(label_y))
        self.add( masa1,resorte_1, ref_masa_1, dibujo_anclaje_1,trayectoria_1)


        # Animación: transcurren 10 segundos
        self.play(tiempo.animate.set_value(8), run_time=8, rate_func=linear)
        self.wait()
