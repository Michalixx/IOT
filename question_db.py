#questions = [["Pyt1", "a", "b", "c", "d", "a"], ["Pyt2", "a", "b", "c", "d", "a"], ["Pyt3", "a", "b", "c", "d", "a"], ["Pyt4", "a", "b", "c", "d", "a"], ["Pyt5", "a", "b", "c", "d", "a"]]

#["Treść pytania", "Odp. A", "Odp. B", "Odp. C", "Odp. D", "a/b/c/d - poprawna odpowiedź"]
questions = [
    [
        "Which information is used by routers to forward a data packet toward its destination?",
        "source IP address",
        "destination IP address",
        "source data-link address",
        "destination data-link address",
        "b"
    ],
    [
        "Which IPv4 address can a host use to ping the loopback interface?",
        "126.0.0.1",
        "127.0.0.0",
        "126.0.0.0",
        "127.0.0.1",
        "d"
    ],
    [
        "Which statement describes a feature of the IP protocol?",
        "IP encapsulation is modified based on network media.",
        "IP relies on Layer 2 protocols for transmission error control.",
        "MAC addresses are used during the IP packet encapsulation.",
        "IP relies on upper layer services to handle situations of missing or out-of-order packets.",
        "d"
    ],
    [
        "Which parameter does the router use to choose the path to the destination when there are multiple routes available?",
        "the lower metric value that is associated with the destination network",
        "the lower gateway IP address to get to the destination network",
        "the higher metric value that is associated with the destination network",
        "the higher gateway IP address to get to the destination network",
        "a"
    ],
    [
        "What is a basic characteristic of the IP protocol?",
        "connectionless",
        "media dependent",
        "user data segmentation",
        "reliable end-to-end delivery",
        "a"
    ],
    [
        "Which field in the IPv4 header is used to prevent a packet from traversing a network endlessly?",
        "Time-to-Live",
        "Sequence Number",
        "Acknowledgment Number",
        "Differentiated Services",
        "a"
    ],
    [
        "What IPv4 header field identifies the upper layer protocol carried in the packet?",
        "Protocol",
        "Identification",
        "Version",
        "Differentiated Services",
        "a"
    ],
    [
        "What routing table entry has a next hop address associated with a destination network?",
        "directly-connected routes",
        "local routes",
        "remote routes",
        "C and L source routes",
        "c"
    ],
    [
        "When transporting data from real-time applications, such as streaming audio and video, which field in the IPv6 header can be used to inform the routers and switches to maintain the same path for the packets in the same conversation?",
        "Next Header",
        "Flow Label",
        "Traffic Class",
        "Differentiated Services",
        "b"
    ],
    [
        "Which destination address is used in an ARP request frame?",
        "0.0.0.0",
        "255.255.255.255",
        "FFFF.FFFF.FFFF",
        "AAAA.AAAA.AAAA",
        "c"
    ]

]

def get_questions():
    return questions