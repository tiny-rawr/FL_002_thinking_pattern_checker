# Mapping of thinking patterns to their corresponding colors.
pattern_color_map = {
    "Black or white thinking": "#FFD1DC",  # Pastel Pink
    "Overgeneralisation": "#FFD1A1",  # Pastel Orange
    "Mental filter": "#FFFFA1",  # Pastel Yellow
    "Discounting the positives": "#A1FFA1",  # Pastel Green
    "Mind reading": "#A1FFFF",  # Pastel Blue
    "Fortune telling": "#D1A1FF",  # Pastel Purple
    "Catastrophising": "#D3D3D3",  # Pastel Grey
    "Emotional reasoning": "#A1FFD1",  # Pastel Cyan
    "Should statements": "#FFA1FF",  # Pastel Magenta
    "Labelling": "#D2B48C",  # Pastel Brown
    "Blaming": "#C0FF3E"  # Pastel Lime
}

# CSS styling for tooltips.
tooltip_style = '''
<style>
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip span {
  display: inline;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 300px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 125%; /* Position the tooltip above the text */
  left: 50%;
  margin-left: -150px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
'''