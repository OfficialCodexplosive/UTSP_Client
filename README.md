# Universal Time Series Provider Client

This is a client library that helps in sending requests to the Universal Time Series Provider, a REST service providing a uniform interface for different time series providers.
Look into the examples folder for several usage examples.

# Basic idea
 
 - specify what load profile you need
 - send the request as json via REST to the utsp
 - it looks into the database if it already has a profile for your request
 - if there is already a profile, it will deliver the profile
 - if there is no profile it will generate one and save it to the database
 - then it will deliver the profile via REST
 
# Notes

- Every request contains a guid string. This can be whatever you want. This guid is part of the database lookup and can be used to enforce recalculation of an otherwhise identical request. This might be interesting if the respective provider has probabilistic components. So if you want a fresh profile every time, ask the utsp with a different guid every time.

# License

MIT License

Copyright (C) 2020 Noah Pflugradt (FZJ IEK-3), David Neuroth (FZJ IEK-3) Leander Kotzur (FZJ IEK-3), Detlef Stolten (FZJ IEK-3)

You should have received a copy of the MIT License along with this program.
If not, see https://opensource.org/licenses/MIT

# About Us 

We are the [Institute of Energy and Climate Research: Techno-Economic Energy Systems Analysis (IEK-3)](https://www.fz-juelich.de/en/iek/iek-3) belonging to the [Forschungszentrum Jülich](https://www.fz-juelich.de/). Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

# Acknowledgement

This work was supported by the Helmholtz Association in the context of the ["Energy System Design"](https://www.helmholtz.de/en/research/research-fields/energy/energy-system-design/) program.

<a href="https://www.helmholtz.de/en/"><img src="https://www.helmholtz.de/fileadmin/user_upload/05_aktuelles/Marke_Design/logos/HG_LOGO_S_ENG_RGB.jpg" alt="Helmholtz Logo" width="200px" style="float:right"></a>
