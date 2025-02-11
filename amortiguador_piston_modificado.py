from manim import *
import numpy as np

class SinAmortiguamiento(Scene):
    def construct(self):

        #############Aparece Ec. de mov Amortiguado
        ecuacion1 = MathTex("x(t) = A \\cos(\\omega t)")
        ecuacion1.to_edge(UP)
        self.play(Write(ecuacion1))

        # Configuración de la gráfica del MAS
        grafica = Axes(x_range=[0, 6, 1], y_range=[-1.5, 1.5, 0.5], axis_config={"include_numbers": True, "color": WHITE}).scale(0.5)
        grafica.to_edge(LEFT)

        # Parámetros del sistema
        SHIFT_MASA = 8 * RIGHT  
        A, w, epsilon = 1, 15, 0  # Amplitud y frecuencia angular
        tiempo = ValueTracker(0)
        desf_trans = 0  ##desfase para mover resorte y amortiguador

        # Masa y anclaje
        masa = Rectangle(width=0.8, height=0.4, color=BLUE, fill_opacity=1).move_to(grafica.c2p(0, 0) + SHIFT_MASA)
        anclaje_coord = grafica.c2p(0, 1.5) + SHIFT_MASA
        dibujo_anclaje = Rectangle(width=1, height=0.1, color=DARK_GRAY, fill_opacity=0.9).move_to(anclaje_coord)

        # Parámetros de la cicloide
        a, k = 0.05, 2

        def actualizar_cicloide(desf_trans=0):
            t = np.linspace(0, 18, 100)
            y_masa = masa.get_center()[1]
            return VMobject().set_points_as_corners([
                grafica.c2p(a * (1 - k * np.cos(ti)), np.interp(ti, [0, 18], [anclaje_coord[1], y_masa])) + SHIFT_MASA + RIGHT*desf_trans
                for ti in t
            ]).set_color(GRAY)

        resorte = always_redraw(actualizar_cicloide)
        ref_masa = always_redraw(lambda: DashedLine([grafica.c2p(tiempo.get_value(), 0)[0], masa.get_center()[1], 0], masa.get_center(), color=RED))
        trayectoria = VGroup()
        
        def calculo_amplitud(t):
            return A * np.exp(-epsilon * t) * np.sin(w * t)

        def actualizar_masa(m):
            t = tiempo.get_value()
            m.move_to(grafica.c2p(0, calculo_amplitud(t)) + SHIFT_MASA)

        def actualizar_trayectoria(tray):
            t = tiempo.get_value()
            tray.add(Dot(grafica.c2p(tiempo.get_value(), calculo_amplitud(t)), radius=0.03, color=YELLOW))

        masa.add_updater(actualizar_masa)
        trayectoria.add_updater(actualizar_trayectoria)

        # Agregar elementos y animar
        self.add(grafica, resorte, masa, ref_masa, trayectoria, dibujo_anclaje)
        self.play(tiempo.animate.set_value(5), run_time=5, rate_func=linear)
        self.wait()




        # Se limpia la animacion

        tiempo.set_value(0)
        trayectoria.clear_updaters()  # Detiene cualquier animación automática
        self.play(FadeOut(trayectoria))  # Borra con animación
        trayectoria.become(VGroup())  # Deja el VGroup vacío
        #################################################
        #SEGUNDA ANIMACION, MOV AMORTIGUADO
        #################################################

        ecuacion2 = MathTex("x(t) = A e^{-\\gamma t} \\cos(\\omega t)")
        ecuacion2.to_edge(UP)
        self.play(Transform(ecuacion1, ecuacion2))
        A, w, epsilon = 1, 15, 0.7  # Amplitud y frecuencia angular
        ####Resorte 2 para mover el resorte 1
        resorte2 = always_redraw(lambda: actualizar_cicloide(desf_trans=0.2))

        ###Amortiguador
        # Amortiguador (cilindro + pistón dinámico)
        amortiguador_cuerpo = Rectangle(width=0.2, height=0.8, color=GRAY, fill_opacity=1).move_to(anclaje_coord + DOWN * 0.4 + LEFT*0.2)
        amortiguador_piston = always_redraw(lambda: Line(anclaje_coord + DOWN * 0.8 + LEFT*0.2, masa.get_center() +LEFT*0.2, color=WHITE, stroke_width=4))
        amortiguador_cabeza = always_redraw(lambda: Rectangle(width=0.2, height=0.1, color=WHITE, fill_opacity=1).move_to(masa.get_center() + UP * 0.05 + LEFT*0.2))
        

        self.play(Transform(resorte, resorte2))
        self.remove(resorte)
        self.add(resorte2)
        self.bring_to_front(masa)  # Luego traemos la masa al frente
        self.wait()
        self.play(FadeIn(amortiguador_cuerpo, amortiguador_piston, amortiguador_cabeza))
        self.wait()
 
        masa.add_updater(actualizar_masa)
        trayectoria.add_updater(actualizar_trayectoria)


        # # Agregar elementos y animar
        self.add(trayectoria)
        self.play(tiempo.animate.set_value(5), run_time=5, rate_func=linear)
        self.wait()



