from pypevoc.speech.glottal import iaif_ola


def get_glottal_flow(audio, rate):
    """
    获取声门波
    :param audio:
    :param rate:
    :return:
            g:  glottal volume velocity waveform
            dg: glottal volume velocity derivative waveform
            vt:  LPC coefficients of vocal tract
            gf: LPC coefficients of source spectrum
    """
    g, dg, vt, gf = iaif_ola(audio, Fs=rate)
    return g, dg, vt, gf
