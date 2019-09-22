from feature_extraction.glottal_flow import get_glottal_flow
import tools.load_utils as loader
import tools.drawer_utils as drawer
import numpy as np

rate, audio = loader.get_audio()

g, dg, vt, gf = get_glottal_flow(audio, rate)

drawer.plot_array(audio)
drawer.plot_array(g)
drawer.plot_array(dg)
drawer.plot_colorbar(np.transpose(vt))
drawer.plot_colorbar(np.transpose(gf))
