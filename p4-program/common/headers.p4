// headers.p4
#ifndef HEADERS_P4
#define HEADERS_P4

// Standard headers
#include <core.p4>
#include <v1model.p4>

// Ethernet header
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

// IPv4 header
header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

// Voting header
header vote_t {
    bit<2>  decision; // 0: Abstain, 1: Allow, 2: Drop
    bit<6>  reserved;
}

// Header stack for votes (if multiple votes need to be stored)
header_stack vote_t votes[10];

// Define metadata
struct metadata_t {
    bit<8> vote_count_allow;
    bit<8> vote_count_drop;
    bit<8> vote_count_abstain;
}

#endif