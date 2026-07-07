from components.ui.slider import slider

COMPOSITION = slider.root(
    slider.control(
        slider.track(
            slider.indicator(),
            slider.thumb(),
        ),
    ),
)
