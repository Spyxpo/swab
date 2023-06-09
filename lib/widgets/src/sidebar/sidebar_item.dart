import 'package:flutter/material.dart';

class SidebarItem {
  SidebarItem({
    required this.text,
    required this.icon,
    this.children = const [],
  });

  final String text;

  final IconData icon;

  final List<SidebarChildItem> children;
}

class SidebarChildItem {
  SidebarChildItem({
    required this.text,
    required this.icon,
  });

  final String text;

  final IconData icon;
}
