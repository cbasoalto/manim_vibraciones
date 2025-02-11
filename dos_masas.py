from manim import *
import numpy as np

class DosMasas(Scene):
    def construct(self):
        self.camera.background_color = WHITE  
        #-----------------------------------------------#
        # 1) PRIMERA PARTE: Animación Movimiento Sin Amortiguamiento
        #-----------------------------------------------#

        # Ecuación inicial (no amortiguado)
        ecuacion1 = MathTex("x(t) = A \\cos(\\omega t-\\phi) ", color = DARK_BLUE)
        ecuacion1.to_edge(UP)
        self.play(Write(ecuacion1))

        # ECUACIÓN CON VALORES ESPECÍFICOS
        ecuacion_numerica = MathTex(r"x(t) = 1 \cos(3 t - \phi)", color=DARK_BLUE)
        ecuacion_numerica.to_edge(UP)

         # Create axes with dark blue axes lines
        grafica = Axes(
            x_range=[0, 5, 1], 
            y_range=[-1, 1.5, 0.5],
            axis_config={"color": DARK_BLUE},  # color for the axis lines
            tips=True
        ).scale(0.5)
        grafica.to_edge(LEFT)

        
        # Add numerical labels (coordinate labels) along each axis
        grafica.add_coordinates().scale(0.8)
        
        # Grab the coordinate label group and set it to dark blue
        coordinate_labels = grafica.get_coordinate_labels()
        coordinate_labels.set_color(DARK_BLUE)
        label_x = MathTex("t \, sec", color = DARK_BLUE).scale(0.8)  # Reduce tamaño de la etiqueta
        label_y = MathTex("x \, cm", color = DARK_BLUE).scale(0.8)  # Reduce tamaño de la etiqueta
        label_x.move_to(grafica.coords_to_point(5, -0.25))
        label_y.move_to(grafica.coords_to_point(-0.5,1.5))

        # Grab the coordinate label group and set it to dark blue
        coordinate_labels = grafica.get_coordinate_labels()
        coordinate_labels.set_color(DARK_BLUE)

        
        # Parámetros del sistema (primer sistema)
        SHIFT_MASA_1 = 8 * RIGHT   # Desplaza la masa en la escena
        A1, w1, epsilon1 = 1, 3, 0  # Amplitud y frecuencia (sin amortiguamiento)
        
        # Parámetro de tiempo
        tiempo = ValueTracker(0)

        # Masa y anclaje (primer sistema)
        masa1 = Rectangle(width=0.8, height=0.4, color=BLUE, fill_opacity=1)
        masa1.move_to(grafica.c2p(0, 0) + SHIFT_MASA_1)
        
        anclaje_coord_1 = grafica.c2p(0, 1.5) + SHIFT_MASA_1
        dibujo_anclaje_1 = Rectangle(width=1, height=0.1, color=DARK_GRAY, fill_opacity=0.9)
        dibujo_anclaje_1.move_to(anclaje_coord_1)
        
        ##escribir valor de phi
        valor_phi1 = MathTex(r"\phi = 0 \, \text{rad}", color=DARK_BLUE).scale(0.8)
        valor_phi2 = MathTex(r"\phi = \frac{\pi}{3} \, \text{rad}", color=DARK_BLUE).scale(0.8)
        valor_phi1.move_to(anclaje_coord_1 + UP * 0.5)
 
        
        
        # Funciones de movimiento
        def calculo_amplitud_1(t):
            return A1 * np.exp(-epsilon1*t) * np.sin(w1 * t)

        def actualizar_masa_1(m):
            t = tiempo.get_value()
            # y(t) según la ecuación de masa1
            m.move_to(grafica.c2p(0, calculo_amplitud_1(t)) + SHIFT_MASA_1)


        trayectoria_linea = VMobject()
        trayectoria_linea.set_stroke(color=BLUE, width=2)
        puntos =[]
        def actualizar_linea(mobj):
            t = tiempo.get_value()

            nueva_coord = grafica.c2p(t, calculo_amplitud_1(t))
            puntos.append(nueva_coord)
            mobj.set_points_as_corners(puntos)
        trayectoria_linea.add_updater(actualizar_linea)
        self.add(trayectoria_linea)

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

        #-----------------------------------------------#
        #  AGREGAR EL SEGUNDO SISTEMA CON DESFASE
        #-----------------------------------------------#

        # =============== Parámetros 2da masa =============== #
        SHIFT_MASA_2 = SHIFT_MASA_1 + 3*RIGHT  # Más a la derecha
        A2, w2, epsilon2 = 1, 3, 0
        # Definimos un desfase en FASE (puede ser en radianes o en tiempo).
        # Por ej., phi = pi/2 => desfase de 90°
        phi = -PI/3

        # Ecuación de movimiento para la masa 2 (con fase extra)
        def calculo_amplitud_2(t):
            return A2 * np.exp(-epsilon2*t) * np.cos(w2*t+phi)

        # Creamos la masa 2
        masa2 = Rectangle(width=0.8, height=0.4, color=GREEN, fill_opacity=1)
        masa2.move_to(grafica.c2p(0, 0.5) + SHIFT_MASA_2)

        # Anclaje 2
        anclaje_coord_2 = grafica.c2p(0, 1.5) + SHIFT_MASA_2
        dibujo_anclaje_2 = Rectangle(width=1, height=0.1, color=DARK_GRAY, fill_opacity=0.9)
        dibujo_anclaje_2.move_to(anclaje_coord_2)
        valor_phi2.move_to(anclaje_coord_2+UP*0.5)

        # Updater para masa2
        def actualizar_masa_2(m):
            t = tiempo.get_value()
            y = calculo_amplitud_2(t)
            m.move_to(grafica.c2p(0, y) + SHIFT_MASA_2)

        masa2.add_updater(actualizar_masa_2)


        trayectoria_linea = VMobject()
        trayectoria_linea.set_stroke(color=BLUE, width=2)
        puntos =[]
        def actualizar_linea(mobj):
            t = tiempo.get_value()

            nueva_coord = grafica.c2p(t, calculo_amplitud_1(t))
            puntos.append(nueva_coord)
            mobj.set_points_as_corners(puntos)
        trayectoria_linea.add_updater(actualizar_linea)
        self.add(trayectoria_linea)

        
        # # Trayectoria masa 2
        # trayectoria_2 = VGroup()
        # def actualizar_trayectoria_2(tray):
        #     t = tiempo.get_value()
        #     y = calculo_amplitud_2(t)
        #     tray.add(
        #         Dot(
        #             grafica.c2p(t, y),
        #             radius=0.03,
        #             color=GREEN
        #         )
        #     )

        # trayectoria_2.add_updater(actualizar_trayectoria_2)

        trayectoria_linea2 = VMobject()
        trayectoria_linea2.set_stroke(color=GREEN, width=2)
        puntos2 =[]
        def actualizar_linea2(mobj):
            t = tiempo.get_value()
            nueva_coord2 = grafica.c2p(t, calculo_amplitud_2(t))
            puntos2.append(nueva_coord2)
            mobj.set_points_as_corners(puntos2)
        trayectoria_linea2.add_updater(actualizar_linea2)
        self.add(trayectoria_linea2)


        def actualizar_cicloide2(desf_trans=0):
            t = np.linspace(0, 18, 100)
            y_masa2 = masa2.get_center()[1]
            return VMobject().set_points_as_corners([
                grafica.c2p(a * (1 - k * np.cos(ti)), np.interp(ti, [0, 18], [anclaje_coord_2[1]+0.3, y_masa2+0.4])) + SHIFT_MASA_2 + RIGHT*desf_trans
                for ti in t
            ]).set_color(GRAY)
        
        resorte_2 = always_redraw(actualizar_cicloide2) 

                # Línea de referencia en x(t)
        ref_masa_2 = always_redraw(
            lambda: DashedLine(
                [grafica.c2p(tiempo.get_value(), 0)[0], masa2.get_center()[1], 0],
                masa2.get_center(), 
                color=GREEN
            )
        )

        # resorte_2 = always_redraw(generar_resorte_2)

        # Activamos los updaters
        masa1.add_updater(actualizar_masa_1)

        # Agregamos a la escena
        self.play(Create(grafica), run_time=0.5)  # Dibuja la gráfica en 2 segundos
        # trayectoria_1.add_updater(actualizar_trayectoria_1)
        self.play(Write(label_x), Write(label_y))
        self.add( masa1,resorte_1, ref_masa_1, dibujo_anclaje_1)
        
        self.add(masa2, resorte_2, ref_masa_2, dibujo_anclaje_2)
        # self.bring_to_front(masa1) 
        self.wait(2)
        self.play(Write(valor_phi1))
        self.play(Write(valor_phi2))
        # ANIMACIÓN 2: Transformar a la ecuación con valores antes de mostrar el gráfico
        self.play(TransformMatchingTex(ecuacion1, ecuacion_numerica))
        self.wait(1)

        # Animación: transcurren 10 segundos
        self.play(tiempo.animate.set_value(4), run_time=10, rate_func=linear)
        self.wait()

        #-----------------------------------------------#
        # 2) Limpiamos la animación anterior
        #-----------------------------------------------#
        # tiempo.set_value(0)
        # trayectoria_1.clear_updaters() 
        # self.play(FadeOut(trayectoria_1))
        # trayectoria_1.become(VGroup())  # VGroup vacío
        # self.wait()

        # #-----------------------------------------------#
        # # 3) SEGUNDA PARTE: Movimiento Amortiguado
        # #-----------------------------------------------#
        # ecuacion2 = MathTex("x(t) = A e^{-\\gamma t} \\cos(\\omega t)")
        # ecuacion2.to_edge(UP)
        # self.play(Transform(ecuacion1, ecuacion2))
        
        # # Actualizamos parámetros para la segunda animación (primer sistema)
        # A1, w1, epsilon1 = 1, 15, 0.7  # ahora sí con amortiguamiento

        # def calculo_amplitud_1(t):
        #     # Sobrescribimos la función con amortiguamiento
        #     return A1 * np.exp(-epsilon1*t) * np.sin(w1 * t)

        # # Resorte actual con amortiguamiento
        # # (solo para que se note un cambio en la forma, p.e. una leve traslación)
        # def generar_resorte_1_amort():
        #     anclaje = anclaje_coord_1
        #     masa_pos = masa1.get_center()
        #     n_puntos = 20
        #     line = VMobject()
        #     line.set_points_smoothly([
        #         anclaje + (i/(n_puntos-1))*(masa_pos - anclaje)
        #         + UP*0.2*np.sin(6*PI*i/(n_puntos-1))
        #         + 0.1*LEFT  # un "ligero" desplazamiento
        #         for i in range(n_puntos)
        #     ])
        #     line.set_color(GRAY)
        #     return line

        # nuevo_resorte_1 = always_redraw(generar_resorte_1_amort)

        # self.play(Transform(resorte_1, nuevo_resorte_1))
        # self.remove(resorte_1)
        # self.add(nuevo_resorte_1)
        # self.bring_to_front(masa1)
        # self.wait()

        # # Amortiguador para el primer sistema
        # amortiguador_cuerpo_1 = Rectangle(width=0.2, height=0.8, color=GRAY, fill_opacity=1)
        # amortiguador_cuerpo_1.move_to(anclaje_coord_1 + DOWN * 0.4 + LEFT*0.2)
        
        # amortiguador_piston_1 = always_redraw(
        #     lambda: Line(
        #         anclaje_coord_1 + DOWN * 0.8 + LEFT*0.2,
        #         masa1.get_center() + LEFT*0.2,
        #         color=WHITE, stroke_width=4
        #     )
        # )
        # amortiguador_cabeza_1 = always_redraw(
        #     lambda: Rectangle(width=0.2, height=0.1, color=WHITE, fill_opacity=1)
        #     .move_to(masa1.get_center() + UP * 0.05 + LEFT*0.2)
        # )
        
        # self.play(
        #     FadeIn(amortiguador_cuerpo_1, amortiguador_piston_1, amortiguador_cabeza_1)
        # )
        # self.wait()

        # # Reactivamos el updater de la masa 1 y de su trayectoria
        # masa1.add_updater(actualizar_masa_1)
        # trayectoria_1.add_updater(actualizar_trayectoria_1)
        # self.add(trayectoria_1)


        # # Amortiguador 2
        # amortiguador_cuerpo_2 = Rectangle(width=0.2, height=0.8, color=GRAY, fill_opacity=1)
        # amortiguador_cuerpo_2.move_to(anclaje_coord_2 + DOWN * 0.4 + LEFT*0.2)

        # amortiguador_piston_2 = always_redraw(
        #     lambda: Line(
        #         anclaje_coord_2 + DOWN * 0.8 + LEFT*0.2,
        #         masa2.get_center() + LEFT*0.2,
        #         color=WHITE,
        #         stroke_width=4
        #     )
        # )
        # amortiguador_cabeza_2 = always_redraw(
        #     lambda: Rectangle(width=0.2, height=0.1, color=WHITE, fill_opacity=1)
        #     .move_to(masa2.get_center() + UP * 0.05 + LEFT*0.2)
        # )

        # # Agregamos todo el segundo sistema a la escena
        # self.add(
        #     masa2, dibujo_anclaje_2, resorte_2,
        #     amortiguador_cuerpo_2, amortiguador_piston_2, amortiguador_cabeza_2,
        #     trayectoria_2
        # )

        # #-----------------------------------------------#
        # # 5) Ejecutamos la animación final con ambos sistemas
        # #-----------------------------------------------#
        # # Ambos se mueven simultáneamente con el mismo "tiempo",
        # # pero masa2 está desfasada en fase (phi) con respecto a masa1.
        # # Hacemos la misma animación que en el 1er sistema: 5 segundos
        # self.play(tiempo.animate.set_value(5), run_time=5, rate_func=linear)
        # self.wait()
