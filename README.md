## Reproducibility of Firmware Analysis: An Empirical Study

### Background

In recent years, the rapid growth of embedded systems and Internet of Things (IoT) devices has significantly increased cybersecurity threats. Firmware binaries, which contain the essential software controlling hardware operations, are critical components of these systems. As firmware-based devices become increasingly common across industries, ensuring their security has become a major priority for cybersecurity researchers.

**Firmware binary analysis** plays a crucial role in identifying vulnerabilities, detecting malware, and understanding the complex operations of embedded systems. Key analysis tasks include:

- **Reverse engineering:** Identifying firmware properties, such as the image base—the starting address at which an executable is loaded into memory.
- **Software Composition Analysis (SCA):** Identifying embedded third-party libraries (TPLs) and other software components.

### Research Problem

Despite the growing importance of firmware security, questions remain about the effectiveness and reproducibility of existing analysis methods. Reproducibility refers to the ability to replicate research results consistently across different studies and experimental environments.

Firmware analysis presents several challenges due to the complexity of firmware binaries and the diversity of hardware architectures. Independent vulnerability research also faces obstacles such as limited data availability, encrypted firmware images, and hardware heterogeneity.

As firmware-based devices become increasingly prevalent in critical infrastructure and other industries, it is essential to evaluate whether established cybersecurity methods can be reliably reproduced and trusted.

### Research Objectives

This paper presents an empirical investigation into the reproducibility of cybersecurity methods designed for firmware binary analysis.

While previous research has explored various reproducibility challenges in firmware analysis, this study focuses on empirically evaluating the reliability and effectiveness of existing methodologies when applied to accessible firmware images.

The study aims to demonstrate that descriptions of firmware analysis methods in existing research often lack sufficient detail and quality to enable the effective replication of reported results.

### Methodology

To investigate these challenges, we examine a selection of commonly used cybersecurity methods for firmware binary analysis, covering both reverse engineering and Software Composition Analysis (SCA).

The study follows two complementary approaches:

1. **Empirical evaluation:** Conducting systematic experiments and analyses using selected methods across various firmware binaries to assess whether the reported results can be reproduced.
2. **Theoretical evaluation:** Examining the reproducibility of the original studies based on their descriptions of methods, experimental procedures, and reported results.

### Key Findings and Contributions

The findings highlight the challenges and opportunities associated with reproducibility in firmware analysis. The study contributes to the broader discussion of cybersecurity research methodologies by examining the extent to which existing firmware analysis techniques can be independently reproduced.

### Publication

📄 **Read the full paper:** [Reproducibility of Firmware Analysis: An Empirical Study](https://jyx.jyu.fi/bitstreams/c7270281-c4de-4544-b665-1670a133e340/download)
