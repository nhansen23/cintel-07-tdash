import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
from shinyswatch import theme
import plotly.express as px
import palmerpenguins 

# Set Theme
theme.sandstone

df = palmerpenguins.load_penguins()

# Page Layout
ui.page_opts(title="Penguins Dashboard", fillable=True)

# Setup up the sidebar with inputs and website links
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/nhansen23/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://nhansen23.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/nhansen23/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
   # Comment out last URL
   # ui.a(
   #     "See also",
   #     href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
   #     target="_blank",
   # )

# Set up the layout of the data cards
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"),theme="bg-blue"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-blue"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-blue"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Build out the chart 
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length and Depth", class_="p-3 mb-2 bg-secondary text-white")
     # Comment out the original plot
     #   @render.plot
     #   def length_depth():
     #       return sns.scatterplot(
     #           data=filtered_df(),
     #           x="bill_length_mm",
     #           y="bill_depth_mm",
     #           hue="species",
     #       )
    
     # Updating plot to interactive plotly   
        @render_plotly
        def hist():
            df = filtered_df()
            return px.histogram(
                df,
                x="species",
                color="species",
                )

    # Build out the data table
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data", class_="p-3 mb-2 bg-secondary text-white")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

# Create the reactive calc
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
