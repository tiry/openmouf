"""Visualization module for the Mouf emotion engine."""

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.plotting import plot_polygon

from mouf.engine import data_utils
from mouf.engine.emotion import MoufEmotionEngine


class MoufEmotionViz:
    """
    Visualization handler for the Mouf emotion engine.
    
    Displays the valence-arousal space with emotional state regions
    and provides interactive buttons to trigger stimuli.
    """
    
    def __init__(self, engine: MoufEmotionEngine) -> None:
        """
        Initialize the visualization.
        
        Args:
            engine: The MoufEmotionEngine instance to visualize
        """
        self.engine: MoufEmotionEngine = engine
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.25)
        
        # Draw static elements - unit disc boundary
        unit_disc = Point(0, 0).buffer(1.0)
        plot_polygon(
            unit_disc, 
            ax=self.ax, 
            add_points=False, 
            facecolor='none', 
            edgecolor='black', 
            linestyle='--'
        )
        
        # Draw emotional state regions
        for name, geom in self.engine.states.items():
            plot_polygon(geom, ax=self.ax, add_points=False, alpha=0.15)
            self.ax.text(
                geom.centroid.x, 
                geom.centroid.y, 
                name, 
                ha='center', 
                va='center', 
                fontsize=8, 
                alpha=0.7
            )
        
        # Initialize particle (current emotion state position)
        self.particle, = self.ax.plot(
            [], [], 'ro', markersize=12, zorder=5, markeredgecolor='white'
        )
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_title("Mouf Engine Visualizer")

        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up interactive buttons for each stimulus."""
        stimuli = data_utils.load_stimulus()
        self.btns: list[Button] = []
        cols = 3
        for i, (label, impulse) in enumerate(stimuli):
            row, col = divmod(i, cols)
            ax_btn = plt.axes([0.1 + col*0.3, 0.12 - row*0.06, 0.25, 0.05])
            btn = Button(ax_btn, label)
            btn.on_clicked(
                lambda event, imp=impulse: self.engine.apply_impulse(imp[0], imp[1])
            )
            self.btns.append(btn)

    def animate(self, frame: int) -> tuple:
        """
        Animation callback for updating the visualization.
        
        Args:
            frame: Animation frame number
            
        Returns:
            Tuple of artists to update
        """
        new_pos = self.engine.update()
        self.particle.set_data([new_pos[0]], [new_pos[1]])
        
        # Update title with dominant state
        active = self.engine.get_active_states()
        state_str = active[0][0] if active else "Neutral"
        self.ax.set_title(f"Mouf Engine - Current State: {state_str}")
        
        return (self.particle,)

    def show(self) -> None:
        """Display the visualization."""
        self.ani = FuncAnimation(self.fig, self.animate, interval=20, blit=True)
        plt.show()


def main() -> None:
    """Run the visualization as a standalone application."""
    # Create the 'brain'
    engine = MoufEmotionEngine()
    
    # Create the 'eyes/hands'
    viz = MoufEmotionViz(engine)
    
    # Run the simulation
    viz.show()


if __name__ == "__main__":
    main()
