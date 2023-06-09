import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:swab/pages/pages.dart';
import 'package:swab/widgets/widgets.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  int activeTab = 0;
  bool deepLinking = false;

  late TextEditingController appNameController = TextEditingController();
  late TextEditingController appPackageController = TextEditingController();
  late TextEditingController urlController = TextEditingController();
  late TextEditingController appDescriptionController = TextEditingController();
  late TextEditingController contactEmailController = TextEditingController();
  late TextEditingController privacyPolicyController = TextEditingController();
  late TextEditingController termsAndConditionController =
      TextEditingController();

  final List<SidebarItem> items = [
    SidebarItem(
      icon: CupertinoIcons.home,
      text: 'Overview',
    ),
    SidebarItem(
      icon: CupertinoIcons.paintbrush,
      text: 'Branding',
    ),
    SidebarItem(
      icon: CupertinoIcons.link,
      text: 'Link Handling',
    ),
    SidebarItem(
      icon: CupertinoIcons.square_stack,
      text: 'Interface',
    ),
    SidebarItem(
      icon: CupertinoIcons.globe,
      text: 'Website Overrides',
    ),
    SidebarItem(
      icon: CupertinoIcons.lock,
      text: 'Permissions',
    ),
    SidebarItem(
      icon: CupertinoIcons.location,
      text: 'Native Navigation',
    ),
    SidebarItem(
      icon: CupertinoIcons.plus_app,
      text: 'Plugins',
    ),
    SidebarItem(
      icon: CupertinoIcons.cloud_download,
      text: 'Build & Download',
    ),
  ];

  @override
  void initState() {
    super.initState();
    setState(() {
      urlController = TextEditingController(text: "https://");
    });
  }

  @override
  void dispose() {
    urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: Stack(
        children: [
          Column(
            children: [
              const SizedBox(height: 50),
              Expanded(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    AnimatedSidebar(
                      switchIconCollapsed: CupertinoIcons.chevron_right_circle,
                      switchIconExpanded: CupertinoIcons.chevron_left_circle,
                      expanded: false,
                      items: items,
                      selectedIndex: activeTab,
                      autoSelectedIndex: false,
                      onItemSelected: (index) =>
                          setState(() => activeTab = index),
                      duration: const Duration(milliseconds: 200),
                      minSize: 90,
                      maxSize: 230,
                      itemIconSize: 18,
                      itemIconColor: Colors.white,
                      itemHoverColor: Colors.grey.withOpacity(0.3),
                      itemSelectedColor: Colors.grey.withOpacity(0.3),
                      itemTextStyle:
                          const TextStyle(color: Colors.white, fontSize: 16),
                      itemSelectedBorder: const BorderRadius.all(
                        Radius.circular(10),
                      ),
                      itemMargin: 16,
                      itemSpaceBetween: 8,
                      header: Image.asset(
                        'assets/images/logo.png',
                        width: 50,
                        height: 50,
                      ),
                    ),
                    mainScreen(),
                    Padding(
                      padding: const EdgeInsets.only(
                          top: 20.0, bottom: 15.0, right: 15.0),
                      child: Container(
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(166, 57, 57, 57),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: Colors.grey.withOpacity(0.3),
                            width: 1,
                          ),
                        ),
                        child: const SingleChildScrollView(
                          child: Padding(
                            padding: EdgeInsets.only(left: 15.0, right: 15.0),
                            child: Simulator(url: 'https://www.spyxpo.com'),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          Stack(
            children: [
              Container(
                height: 50,
                decoration: const BoxDecoration(
                  color: Color.fromARGB(166, 57, 57, 57),
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(20),
                    bottomRight: Radius.circular(20),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Color.fromRGBO(12, 12, 12, 0.749),
                      spreadRadius: 0,
                      blurRadius: 5,
                      offset: Offset(0, 5),
                    ),
                  ],
                ),
              ),
              const Positioned(
                top: 8,
                left: 20,
                child: Text(
                  'SWAB',
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 30,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget mainScreen() {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.only(right: 15.0, top: 18.0, bottom: 18.0),
        child: Container(
          decoration: BoxDecoration(
            color: const Color.fromARGB(166, 57, 57, 57),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: Colors.grey.withOpacity(0.3),
              width: 1,
            ),
          ),
          child: IndexedStack(
            index: activeTab,
            children: [
              // Overview
              ScrollConfiguration(
                behavior:
                    ScrollConfiguration.of(context).copyWith(scrollbars: false),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      const SizedBox(height: 10),
                      const Padding(
                        padding: EdgeInsets.only(left: 25.0, top: 10.0),
                        child: Column(
                          children: [
                            Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Overview',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 10),
                            Row(
                              children: [
                                Text(
                                  'Configure your app\'s basic settings',
                                  style: TextStyle(
                                    color: Colors.grey,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 10),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'App Name',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.app_badge,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appNameController,
                            placeholder: 'Enter App Name',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'App Package Name',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.cube_box,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appPackageController,
                            inputFormatters: [
                              FilteringTextInputFormatter.deny(
                                RegExp(r"\s\b|\b\s"),
                              ),
                            ],
                            placeholder: 'com.example.app',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Website URL',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.link,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            inputFormatters: [
                              FilteringTextInputFormatter.deny(
                                RegExp(r"\s\b|\b\s"),
                              ),
                            ],
                            controller: urlController,
                            placeholder: 'https://www.example.com',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            onSubmitted: (value) {
                              setState(() {
                                urlController.text = value;
                              });
                            },
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'App Description',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding:
                                  EdgeInsets.only(left: 10.0, bottom: 23.0),
                              child: Icon(
                                CupertinoIcons.text_bubble,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appDescriptionController,
                            maxLength: 200,
                            placeholder: 'Enter App Description',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            maxLines: 2,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Contact Email',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.mail,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            controller: contactEmailController,
                            placeholder: 'contact@example.com',
                            inputFormatters: [
                              FilteringTextInputFormatter.deny(
                                RegExp(r"\s\b|\b\s"),
                              ),
                            ],
                            keyboardType: TextInputType.emailAddress,
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Privacy Policy URL',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.doc,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: privacyPolicyController,
                            placeholder: 'Privacy Policy URL',
                            inputFormatters: [
                              FilteringTextInputFormatter.deny(
                                RegExp(r"\s\b|\b\s"),
                              ),
                            ],
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Terms & Conditions URL',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.doc,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: termsAndConditionController,
                            placeholder: 'Terms & Conditions URL',
                            inputFormatters: [
                              FilteringTextInputFormatter.deny(
                                RegExp(r"\s\b|\b\s"),
                              ),
                            ],
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 30),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 30),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.6,
                          child: CupertinoButton(
                            padding: const EdgeInsets.all(10),
                            color: Colors.blue,
                            borderRadius: BorderRadius.circular(10),
                            onPressed: () {
                              setState(() {
                                activeTab = 1;
                              });
                            },
                            child: const Text(
                              'Next',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                              ),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                    ],
                  ),
                ),
              ),
              // Branding
              ScrollConfiguration(
                behavior:
                    ScrollConfiguration.of(context).copyWith(scrollbars: false),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      const SizedBox(height: 10),
                      const Padding(
                        padding: EdgeInsets.only(left: 25.0, top: 10.0),
                        child: Column(
                          children: [
                            Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Branding',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 10),
                            Row(
                              children: [
                                Text(
                                  'Customize the look and feel of your app',
                                  style: TextStyle(
                                    color: Colors.grey,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 10),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'App Icon',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'Upload 512x512px PNG file',
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          child: Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: Colors.grey.withOpacity(0.3),
                              ),
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Container(
                                  width: 100,
                                  height: 100,
                                  decoration: BoxDecoration(
                                    color: Colors.grey.withOpacity(0.3),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: const Center(
                                    child: Icon(
                                      CupertinoIcons.add,
                                      color: Colors.white,
                                      size: 40,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                const Text(
                                  'Upload',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Splash Screen',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'Upload 1125x2436px PNG file',
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          child: Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: Colors.grey.withOpacity(0.3),
                              ),
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Container(
                                  width: 300,
                                  height: 550,
                                  decoration: BoxDecoration(
                                    color: Colors.grey.withOpacity(0.3),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: const Center(
                                    child: Icon(
                                      CupertinoIcons.add,
                                      color: Colors.white,
                                      size: 40,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                const Text(
                                  'Upload',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 30),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 30),
                      Center(
                        child: Wrap(
                          runSpacing: 20,
                          children: [
                            Padding(
                              padding:
                                  const EdgeInsets.only(left: 5.0, right: 5.0),
                              child: SizedBox(
                                width: MediaQuery.of(context).size.width * 0.3,
                                child: CupertinoButton(
                                  padding: const EdgeInsets.all(10),
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(10),
                                  onPressed: () {
                                    setState(() {
                                      activeTab = 0;
                                    });
                                  },
                                  child: const Text(
                                    'Back',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 20),
                            Padding(
                              padding:
                                  const EdgeInsets.only(left: 5.0, right: 5.0),
                              child: SizedBox(
                                width: MediaQuery.of(context).size.width * 0.3,
                                child: CupertinoButton(
                                  padding: const EdgeInsets.all(10),
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(10),
                                  onPressed: () {
                                    setState(() {
                                      activeTab = 2;
                                    });
                                  },
                                  child: const Text(
                                    'Next',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 20),
                    ],
                  ),
                ),
              ),
              // Link Handling
              ScrollConfiguration(
                behavior:
                    ScrollConfiguration.of(context).copyWith(scrollbars: false),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      const SizedBox(height: 10),
                      const Padding(
                        padding: EdgeInsets.only(left: 25.0, top: 10.0),
                        child: Column(
                          children: [
                            Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Link Handling',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 10),
                            Row(
                              children: [
                                Text(
                                  'Configure deep linking for your app',
                                  style: TextStyle(
                                    color: Colors.grey,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 10),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'Deep Linking',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'Deep linking allows users to navigate directly to content\n in your app. You can configure deep linking\n for your app by adding intent filters to your AndroidManifest.xml\n and by setting up URL scheme support for your iOS app.',
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 16,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 10),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width,
                          child: ListTile(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                            leading: const Icon(
                              CupertinoIcons.link,
                              size: 16,
                              color: Colors.white,
                            ),
                            title: const Text(
                              'Deep Linking',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                              ),
                            ),
                            trailing: Transform.scale(
                              scale: 0.7,
                              child: CupertinoSwitch(
                                value: deepLinking,
                                onChanged: (value) {
                                  setState(() {
                                    if (deepLinking == false) {
                                      deepLinking = true;
                                    } else {
                                      deepLinking = false;
                                    }
                                  });
                                },
                              ),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 30),
                      Divider(
                        color: Colors.grey.withOpacity(0.3),
                        thickness: 1,
                      ),
                      const SizedBox(height: 30),
                      Center(
                        child: Wrap(
                          runSpacing: 20,
                          children: [
                            Padding(
                              padding:
                                  const EdgeInsets.only(left: 5.0, right: 5.0),
                              child: SizedBox(
                                width: MediaQuery.of(context).size.width * 0.3,
                                child: CupertinoButton(
                                  padding: const EdgeInsets.all(10),
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(10),
                                  onPressed: () {
                                    setState(() {
                                      activeTab = 1;
                                    });
                                  },
                                  child: const Text(
                                    'Back',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 20),
                            Padding(
                              padding:
                                  const EdgeInsets.only(left: 5.0, right: 5.0),
                              child: SizedBox(
                                width: MediaQuery.of(context).size.width * 0.3,
                                child: CupertinoButton(
                                  padding: const EdgeInsets.all(10),
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(10),
                                  onPressed: () {
                                    setState(() {
                                      activeTab = 3;
                                    });
                                  },
                                  child: const Text(
                                    'Next',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 20),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class NotSupported extends StatelessWidget {
  const NotSupported({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image(
            image: AssetImage('assets/images/not-supported.png'),
            width: 400,
          ),
          SizedBox(height: 20),
          Text(
            'Please use a larger screen',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 24,
            ),
          ),
          SizedBox(height: 5),
          Text(
            'The screen size is too small to display the content',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }
}
